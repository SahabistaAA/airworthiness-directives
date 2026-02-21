# Airworthiness Directives (AD) Pipeline

## Overview

The Airworthiness Directives Pipeline is an automated tool designed to ingest, process, and evaluate aviation Airworthiness Directives against a provided fleet of aircraft configurations.

The current pipeline utilizez Hybrid method that combine `ExtractorService` to extract the text from the PDF and then utilize `LLMParser` to parse the text and extract the information. It would make sure robustness of the pipeline and accuracy of the extracted information. This method ensure capabilities of LLM to accurately interpret the complex applicability rules, Manufacturer Serial Number (MSN) constraints, and equipment modifications.

## Features

- **Automated Ingestion**: Reads ADs in PDF format from the `data/raw` directory.
- **Intelligent Parsing**: Leverages Google's `gemini-2.5-pro` (via `google-generativeai`) to extract structured applicability constraints (`ADRules`) into JSON format.
- **Fleet Evaluation**: Matches the parsed rules against an aircraft fleet checking model types, serial numbers, and existing production/service modifications.
- **Output Visualization**: Provides an easy-to-read ASCII table in the terminal displaying whether each aircraft is `✅ Affected`, `❌ Not affected`, or `❌ Not applicable`.

## Prerequisites

- Python 3.9+
- A Google Gemini API Key.

## Installation

1. **Clone the repository** (if applicable) and navigate to the root directory.
2. **Install the package and dependencies** using the provided `pyproject.toml`:
   ```bash
   pip install -e .
   ```
   *(This will install required libraries like `pydantic-settings`, `pymupdf`, `google-generativeai`, `loguru`, `typer` and `click`)*.

3. **Configure Environment Variables**:
   Copy the example environment file:
   ```bash
   cp source/.env.example source/.env
   ```
   Open `source/.env` and insert your Gemini API key:
   ```env
   LLM_API_KEY="your-gemini-api-key-here"
   ```

## How to Run

You can execute the pipeline using the Typer CLI entry point found in `source/main.py`.

Put your raw PDF Airworthiness Directives inside the  `data/raw/` folder, then run:

```bash
python source/main.py
```

### Parsing Modes

The pipeline supports different extraction modes, selectable via the `--mode` flag:

- **`default`** (Recommended): Extracts text using PyMuPDF and parses the logic using the Gemini LLM.
- **`extractor`**: Extracts raw text using PyMuPDF (No LLM parsing - outputs Dummy IDs).
- **`ocr`**: (Placeholder) Extracts text from images using PyTesseract.
- **`vlm`**: (Placeholder) Visual Language Model parsing.
- **`hybrid`**: (Placeholder) Hybrid LLM/VLM parsing.

Example:
```bash
python source/main.py --mode default
python source/main.py --mode extractor
```

## Outputs

- **Structured Data**: The pipeline will save the parsed rules into JSON files inside `data/output/` (e.g. `data/output/2025-0254R1.json`).
- **Terminal Summary**: A table will be printed showing the applicability of the ADs for the test fleet defined in `source/main.py`.

## Future Enhancements
- **extractor**: Fully implement the extractor mode to extract the rules from the ADs by only using regex and string manipulation.
- **ocr**: Fully implement the ocr mode to extract the rules from the ADs by using OCR for scanned documents.
- **vlm**: Fully implement the vlm mode to extract the rules from the ADs by using VLM, it could be complimented with OCR Service.
- **hybrid**: Fully implement the hybrid mode to extract the rules from the ADs by combining the LLM and VLM for extracting information from the ADs. This method would be the default mode in the future, it would be the most robust and accurate method for extracting information from the ADs.