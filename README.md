# Hindi Document RAG Assistant — MegaMindz Level 1

A small, local Retrieval-Augmented Generation (RAG) pipeline for the supplied Hindi study guide about A. P. J. Abdul Kalam. It supports Hindi and English questions, indexes passages in ChromaDB, and returns answers with page, section, chunk ID, and retrieval score citations.

## Features

- PDF text extraction with PyMuPDF, preserving physical PDF page numbers.
- Unicode NFC normalization and whitespace cleanup without stripping Devanagari marks or danda (`।`).
- Sentence/paragraph-aware chunking with overlap.
- Multilingual `intfloat/multilingual-e5-small` embeddings.
- Persistent local ChromaDB vector storage.
- English-to-Hindi cross-lingual retrieval.
- Evidence snippets and automatic metadata citations.
- No paid API key required: the default answer mode selects evidence sentences from retrieved passages. This is an extractive fallback, not an LLM-generated response.
- Six required assignment questions are run by `tests/test_queries.py`.

## Project structure

```text
data/
  Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf
  chroma_db/                 # created by ingestion
src/
  config.py
  ingest.py
  retriever.py
  answer.py
tests/
  test_queries.py
outputs/
  results.md                 # generated test output
requirements.txt
```

## Requirements

- Python 3.10 or 3.11 recommended.
- Internet connection on the first run to install dependencies and download the embedding model.
- A few GB of free disk space is recommended for Python packages and the model cache.
- No paid LLM API key is required.

## Windows + VS Code setup

Open this project folder in VS Code. Open **Terminal → New Terminal** (PowerShell).

### 1. Check Python

```powershell
py --version
```

If this says the command is not recognized, install Python 3.11 from https://www.python.org/downloads/ and select **Add python.exe to PATH** during installation. Restart VS Code and check again.

### 2. Create and activate a virtual environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use this for the current terminal session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Alternative without activation:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Add the supplied PDF

Copy `Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf` into the `data` folder. The expected exact path is:

```text
data\Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf
```

### 5. Build the index

Run from the project root:

```powershell
python -m src.ingest
```

This extracts text, creates chunks, downloads/loads the multilingual embedding model, and writes the ChromaDB index to `data/chroma_db/`. Re-running ingestion rebuilds the collection to avoid duplicate chunks.

### 6. Ask a question

```powershell
python -m src.answer "कलाम को भारत रत्न किस वर्ष प्राप्त हुआ?"
python -m src.answer "Which institution did Kalam attend to study aeronautical engineering?"
```

Append an answer to a log:

```powershell
python -m src.answer "How and where did Kalam die in 2015?" --output outputs\manual_queries.md
```

### 7. Run the six required test queries

```powershell
python -m tests.test_queries
```

Review `outputs/results.md`. Do not submit it without checking that each answer is supported by the cited evidence and that English questions retrieve the correct Hindi passages.

## Design choices

### Chunking

The initial target is 900 characters with 120 characters of overlap. Hindi paragraphs and sentence punctuation (`।`, `.`, `!`, `?`) are respected where possible. Longer units are split as a fallback. The values are starting points; inspect retrieval results and tune if necessary. Chunk IDs are deterministic for the same page, section, order, and content.

### Vector database

ChromaDB was selected because it is open-source, simple to run locally, and supports persistent collections, document metadata, and vector similarity queries without a separate server.

### Hindi handling and embeddings

Text is normalized with Unicode NFC; whitespace is cleaned but Devanagari combining marks and danda are preserved. The multilingual E5 model is used for both Hindi passages and Hindi/English queries. E5's `passage:` and `query:` prefixes are applied as recommended by the model family. Physical PDF page numbers are stored as 1-based metadata. Section labels are inferred from numbered headings at the start of pages; verify these labels in the output because headings that wrap across lines may need refinement.

### Citations

Citations are populated from retrieved ChromaDB metadata at answer time, not manually assigned. Chroma returns cosine distance because the collection is configured with cosine space; the script reports `1 - distance` as a similarity-like score. Treat it as a retrieval score, not a calibrated probability.

### Answer generation and limitations

The default answer function is an extractive, evidence-first fallback so the project runs without a paid LLM key. It is not a generative LLM. Sentence selection is intentionally simple and may need improvement for complex questions. If an accessible local or hosted LLM is later added, pass only retrieved context to it, require it to abstain when evidence is missing, and retain the same citations.

PDF table extraction quality depends on how the PDF encodes text. If rows are fragmented, add a dedicated table extraction/repair step and validate the timeline and awards sections. Retrieval quality should be assessed empirically using the six supplied queries.

## Troubleshooting

- **PDF not found:** check the exact filename and `data` path.
- **PowerShell activation error:** use the process-scoped execution policy command above, or call `.venv\Scripts\python.exe` directly.
- **Model download fails:** check internet access and disk space; retry after connectivity is restored.
- **No collection found:** run `python -m src.ingest` before asking questions.
- **Poor English-to-Hindi retrieval:** inspect top-k evidence; try `TOP_K = 5` or tune chunk size/overlap. Do not hardcode answers to the required questions.

## Submission checklist

- [ ] Ingestion and question answering run end to end.
- [ ] Six-query output is generated from the actual pipeline.
- [ ] Every answer has page, section, chunk ID, and score.
- [ ] English questions retrieve relevant Hindi passages.
- [ ] `requirements.txt` and this README are included.
- [ ] No secrets or virtual environment are committed.
