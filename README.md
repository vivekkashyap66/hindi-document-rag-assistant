# Hindi Document RAG Assistant — MegaMindz Level 1

A local Retrieval-Augmented Generation (RAG) pipeline for the supplied Hindi study guide about A. P. J. Abdul Kalam. The application supports Hindi and English queries, indexes document passages in ChromaDB, and returns evidence-backed answers with source citations, including PDF page number, section, chunk ID, and retrieval score.

## Features

- **PDF processing:** Extracts text from PDF pages using PyMuPDF.
- **Hindi text handling:** Applies Unicode NFC normalization and whitespace cleanup while preserving Devanagari marks and danda (`।`).
- **Chunking:** Splits text into manageable passages using paragraph and sentence boundaries with overlap.
- **Multilingual embeddings:** Uses `intfloat/multilingual-e5-small` for Hindi and English retrieval.
- **Vector database:** Stores embeddings and metadata in a persistent local ChromaDB collection.
- **Cross-lingual retrieval:** Supports English questions over Hindi source content.
- **Evidence and citations:** Returns retrieved evidence snippets with page, section, chunk ID, and retrieval score.
- **Local execution:** Does not require a paid LLM API key.
- **Extractive answering:** Uses a lightweight evidence-based answer function rather than an LLM-generated response.
- **Evaluation:** Provides a script to run the six mandatory assignment queries and save their outputs.

## Project Structure

```text
hindi-document-rag-assistant/
├── data/
│   └── Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf
├── outputs/
│   ├── .gitkeep
│   └── results.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingest.py
│   ├── retriever.py
│   └── answer.py
├── tests/
│   ├── __init__.py
│   ├── test_answer.py
│   └── test_queries.py
├── .gitignore
├── README.md
└── requirements.txt
```

The `data/chroma_db/` directory is created when ingestion runs. It is excluded from Git because the vector index can be regenerated from the supplied PDF.

## Requirements

- Python 3.10 or 3.11 recommended.
- Internet access for installing dependencies and downloading the embedding model on the first run.
- Sufficient disk space for Python dependencies, the model cache, and the generated vector index.
- No paid LLM API key is required.

## Windows Setup Using VS Code

Open the project folder in VS Code and select **Terminal → New Terminal**. The commands below assume PowerShell and that the terminal is in the project root.

### 1. Check Python

```powershell
py --version
py -0p
```

If Python is not installed, install Python 3.11 from [python.org](https://www.python.org/downloads/). Ensure Python is available through the Python launcher.

### 2. Create and Activate a Virtual Environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, allow it for the current terminal session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Alternatively, run Python directly from the virtual environment without activating it:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

### 3. Install Dependencies

With the virtual environment activated, run:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Verify the Dataset

Ensure the supplied PDF is located at:

```text
data/Agni_Ki_Udaan_Adhyayan_Sahayika_Hindi.pdf
```

The PDF is included in the repository. If setting up the project from a different location, copy the supplied document into the `data` directory using the exact filename expected by the application.

### 5. Build the Vector Index

Run this command from the project root:

```powershell
python -m src.ingest
```

The ingestion process extracts the PDF text, normalizes it, creates chunks, generates multilingual embeddings, and stores the indexed passages in `data/chroma_db/`.

Re-run ingestion if the source document or chunking configuration changes.

### 6. Ask Questions

Hindi example:

```powershell
python -m src.answer "कलाम को भारत रत्न किस वर्ष प्राप्त हुआ?"
```

English example:

```powershell
python -m src.answer "Which institution did Kalam attend to study aeronautical engineering?"
```

To save an answer to a separate output file, if supported by the current command-line implementation:

```powershell
python -m src.answer "How and where did Kalam die in 2015?" --output outputs\manual_queries.md
```

### 7. Run the Six Mandatory Assignment Queries

Execute the evaluation script:

```powershell
python -m tests.test_queries
```

The script runs the six required questions through the retrieval and answering pipeline and saves the formatted output to:

```text
outputs/results.md
```

Review the generated file to confirm that each answer is supported by the retrieved evidence and that the source
