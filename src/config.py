from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT_DIR / "data" / "Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf"
CHROMA_PATH = ROOT_DIR / "data" / "chroma_db"
COLLECTION_NAME = "agni_ki_udaan_hindi"
EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
CHUNK_SIZE = 900       # characters; chosen to retain useful context in Hindi paragraphs
CHUNK_OVERLAP = 120    # characters; reduces loss at chunk boundaries
TOP_K = 4
