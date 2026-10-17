"""Extract, normalize, chunk and index the supplied Hindi PDF."""
import re
import unicodedata
import hashlib
from typing import List, Dict

import fitz
import chromadb
from sentence_transformers import SentenceTransformer

from src.config import (
    PDF_PATH, CHROMA_PATH, COLLECTION_NAME, EMBEDDING_MODEL,
    CHUNK_SIZE, CHUNK_OVERLAP,
)

# Headings in the supplied PDF use numbered section labels such as "6 · इसरो के वर्ष..."
HEADING_RE = re.compile(r"^\s*(?:\d{1,2}\s*[·.]?\s*[-–]?\s*)?(.{2,100})\s*$")


def normalize_text(text: str) -> str:
    """Normalize Unicode and whitespace without removing Devanagari marks or danda."""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pages(pdf_path=PDF_PATH) -> List[Dict]:
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}\nPlace the supplied PDF in the project's data folder."
        )
    pages = []
    current_section = "Unlabelled section"
    with fitz.open(pdf_path) as doc:
        for page_index, page in enumerate(doc):
            raw = page.get_text("text", sort=True)
            text = normalize_text(raw)
            if not text:
                continue
            # Capture the first plausible numbered heading on each page.
            for line in text.splitlines()[:8]:
                line = line.strip()
                if re.match(r"^\d{1,2}\s*[·.]", line):
                    current_section = line
                    break
            pages.append({
                "page": page_index + 1,  # physical PDF page number, 1-based
                "section": current_section,
                "text": text,
            })
    return pages


def split_sentences(text: str) -> List[str]:
    """Split on Hindi danda and common sentence punctuation, retaining punctuation."""
    text = normalize_text(text)
    # Paragraph split first, then sentence punctuation; preserve table-like lines.
    pieces = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        sentences = re.split(r"(?<=[।.!?])\s+", paragraph)
        pieces.extend(s.strip() for s in sentences if s.strip())
    return pieces


def chunk_page(page: Dict, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> List[Dict]:
    """Pack sentence units into overlapping chunks; avoid cutting sentences when possible."""
    units = split_sentences(page["text"])
    chunks, current = [], ""
    for unit in units:
        # A long table row or sentence may exceed the target; split only as a fallback.
        if len(unit) > chunk_size:
            if current:
                chunks.append(current.strip())
                current = ""
            start = 0
            while start < len(unit):
                piece = unit[start:start + chunk_size].strip()
                if piece:
                    chunks.append(piece)
                start += max(1, chunk_size - overlap)
            continue
        candidate = f"{current} {unit}".strip() if current else unit
        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current.strip())
            tail = current[-overlap:] if overlap and current else ""
            current = f"{tail} {unit}".strip() if tail else unit
    if current:
        chunks.append(current.strip())

    output = []
    for local_index, content in enumerate(chunks):
        digest = hashlib.sha1(f'{page["page"]}|{page["section"]}|{local_index}|{content}'.encode("utf-8")).hexdigest()[:10]
        output.append({
            "id": f"p{page['page']:03d}_c{local_index:03d}_{digest}",
            "text": content,
            "page": page["page"],
            "section": page["section"][:500],
        })
    return output


def build_chunks(pages: List[Dict]) -> List[Dict]:
    all_chunks = []
    for page in pages:
        all_chunks.extend(chunk_page(page))
    return all_chunks


def main():
    print(f"Reading PDF: {PDF_PATH}")
    pages = extract_pages()
    chunks = build_chunks(pages)
    if not chunks:
        raise RuntimeError("No text chunks extracted. Check whether the PDF is text-based or scanned.")
    print(f"Extracted {len(pages)} non-empty pages and created {len(chunks)} chunks.")

    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    # Rebuild the collection so rerunning ingestion doesn't create duplicate chunks.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    batch_size = 64
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        # E5 expects passage: prefix for document passages.
        texts = [f"passage: {item['text']}" for item in batch]
        vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False).tolist()
        collection.add(
            ids=[item["id"] for item in batch],
            documents=[item["text"] for item in batch],
            embeddings=vectors,
            metadatas=[
                {"page": item["page"], "section": item["section"], "chunk_id": item["id"]}
                for item in batch
            ],
        )
    print(f"Indexed {collection.count()} chunks in {CHROMA_PATH}")
    print("Ingestion complete.")


if __name__ == "__main__":
    main()
