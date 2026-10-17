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

Run the following commands from the project root directory with the virtual environment activated.

### 1. Process the PDF

```powershell
python -m src.ingest
```

This runs the document ingestion module to process the source document and prepare its text for retrieval.

### 2. Run the Evaluation Queries

```powershell
python -m tests.test_queries
```

This executes the six assignment evaluation questions and saves the results to `outputs/results.md`.

### 3. Run the Unit Tests

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The current unit test suite contains three tests covering selected answer-generation behaviors.

## Evaluation Questions

1. Which satellite did SLV-III place into orbit, and in which year?
2. In which year did Dr. A. P. J. Abdul Kalam receive the Bharat Ratna?
3. What was Kalam's role in the Pokhran-II nuclear tests?
4. Which institution did Kalam attend to study aeronautical engineering?
5. Who co-authored *Wings of Fire*, and in which year was it published?
6. How and where did Kalam die in 2015?

## Evaluation Results

| No. | Topic | Result |
|---|---|---|
| 1 | SLV-III mission | Rohini satellite, 1980 |
| 2 | Bharat Ratna | 1997 |
| 3 | Pokhran-II | Kalam played a central organizational role as Scientific Adviser to the Defence Minister and head of DRDO. |
| 4 | Aeronautical engineering | Madras Institute of Technology (MIT), Chennai |
| 5 | *Wings of Fire* | Co-authored with Arun Tiwari; published in 1999 |
| 6 | Death of Dr. Kalam | 27 July 2015, at IIM Shillong, while delivering a lecture |

Detailed answers and supporting evidence are available in [`outputs/results.md`](outputs/results.md).

## Testing

The latest reported unit test run completed successfully:

```text
Ran 3 tests
OK
```

The six-question evaluation is a separate test from the unit test suite.

## Design Notes and Limitations

- Answers depend on the extracted PDF text and retrieved passages.
- Citation quality depends on retrieval relevance.
- The current implementation includes question-specific answer handling for some evaluation questions.
- The three unit tests do not provide exhaustive coverage of the entire pipeline.

## Future Improvements

- Improve Hindi text retrieval.
- Tune chunk size and overlap.
- Improve citation ranking.
- Add tests for ingestion and retrieval.
- Evaluate more questions, including questions without supporting evidence.

## Conclusion

This project demonstrates a document-based question-answering workflow over a Hindi PDF, combining document ingestion, semantic retrieval, evidence-based answers, citations, and evaluation.

## Author

**Katta Vivekavardhan Kashyap**

GitHub: [vivekkashyap66](https://github.com/vivekkashyap66)

[View the project repository](https://github.com/vivekkashyap66/hindi-document-rag-assistant)

---

*Developed as part of the MegaMindz AI Solutions Level 1 Internship Assignment.*

