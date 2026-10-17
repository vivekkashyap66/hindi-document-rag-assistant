# Hindi Document RAG Assistant

A local Retrieval-Augmented Generation (RAG) assistant designed to answer questions from the Hindi PDF *Agni Ki Udaan Adhyayan Sahayika*, a study guide about Dr. A. P. J. Abdul Kalam.

The system extracts text from the PDF, divides it into chunks, retrieves relevant passages for a question, and generates an answer supported by the retrieved document content.

## Project Overview

This project was developed as part of the **MegaMindz AI Solutions – Level 1 Internship Assignment**.

### Objectives

- Build a document-based question-answering system.
- Extract and process text from a Hindi PDF.
- Retrieve relevant document chunks for user queries.
- Generate answers supported by retrieved evidence.
- Evaluate the system using the six mandatory assignment questions.
- Provide source citations to help verify answers.

## Features

- **PDF ingestion:** Extracts text from the supplied Hindi PDF.
- **Text chunking:** Divides extracted text into manageable chunks.
- **Semantic retrieval:** Retrieves relevant passages for each question.
- **Evidence-based answering:** Uses retrieved document content to formulate answers.
- **Source citations:** Includes page references and chunk identifiers where available.
- **Evaluation:** Runs the six mandatory assignment questions.
- **Unit testing:** Tests selected answer-generation behaviors.
- **Evaluation report:** Saves answers and supporting evidence in `outputs/results.md`.

## Technology Stack

- Python 3.10+
- PDF text extraction
- Text chunking
- Embeddings and semantic retrieval
- Vector-based similarity search
- Python `unittest` for testing

The exact dependencies, embedding configuration, and model settings are defined in `requirements.txt` and `src/config.py`.

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
│   ├── test_answer.py
│   └── test_queries.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Requirements

Before running the project, ensure you have:

- Python 3.10 or a compatible newer version
- Git
- Visual Studio Code or another Python-compatible editor
- Internet access for installing dependencies and downloading required models

## Setup and Installation on Windows

### Step 1: Clone the Repository

Open PowerShell or the VS Code terminal and run:

```powershell
git clone https://github.com/vivekkashyap66/hindi-document-rag-assistant.git
cd hindi-document-rag-assistant
```

If you have already cloned the repository, navigate to your existing project directory instead.

### Step 2: Create a Virtual Environment

For Python 3.10:

```powershell
py -3.10 -m venv .venv
```

Alternatively, create the environment using your default Python installation:

```powershell
py -m venv .venv
```

### Step 3: Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run the following command in the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

### Step 5: Verify the Installation

```powershell
python --version
python -m pip --version
```

## Running the Project

Run the following commands from the repository root with the virtual environment activated.

### Step 1: Process
