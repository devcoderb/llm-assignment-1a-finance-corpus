# Assignment 1A: Continued Pretraining and QLoRA

Domain: **Indian Financial Markets and Digital Payments**

This repository contains the implementation for Assignment 1A covering:

- PDF text extraction and corpus cleaning
- Tokenization and packed dataset creation
- Continued Pretraining (CPT)
- Domain evaluation and perplexity comparison
- Instruction dataset generation
- QLoRA supervised fine-tuning
- Base vs CPT vs CPT+QLoRA evaluation

Corpus
The current source corpus contains 10 publicly available financial-domain documents from RBI and SEBI.
The corpus covers topics including:
- Equity derivatives and individual trader behaviour
- Securities buy-back regulation
- Infrastructure Investment Trusts
- Municipal debt securities
- Investor protection
- Digital payments
- UPI
- Payment-system benchmarking and development

Source PDFs are stored under:

`data/corpus/v1/Finance/`

The notebook discovers and processes the available PDF files using relative paths rather than relying on a hardcoded document count.

## Running

Open Assignment-1a.ipynb and execute the notebook cells in order.

The notebook is designed so that the main processing stages can be executed sequentially:
PDF ingestion
- cleaning
- tokenization
- CPT
- CPT evaluation
- instruction dataset
- QLoRA
- final evaluation
- artifact verification

Required Python packages are checked by the notebook and missing dependencies are installed when required.

For Kubeflow execution, the notebook should be run from persistent storage using relative paths and a CUDA-enabled Python environment.

## Generated Outputs

During execution, the notebook creates the required output directories and artifacts, including:
- Raw and cleaned corpus text
- Tokenized and packed CPT dataset
- CPT model checkpoint
- Training-loss plots
- Base and CPT perplexity results
- Instruction dataset JSONL files
- Training and evaluation instruction splits
- QLoRA adapter
- Base / CPT / QLoRA prompt evaluations

A final verification stage checks that the required assignment artifacts are present and that dataset counts are internally consistent.

## Notes

The original PDFs under data/corpus/v1/ are treated as the source corpus and should not be modified during preprocessing.

Cleaning is applied only to derived text files. The pipeline removes or flags low-value extraction artifacts such as:
- table-of-contents material
- repeated headers and footers
- page-number noise
- acknowledgements
- strongly table-dominated extraction

Substantive regulatory content, schedules, annexures, and explanatory sections are retained where they contain useful domain information.


The most useful addition is the architecture block because it immediately explains:

**PDFs → CPT → evaluation → instruction data → QLoRA → final comparison**

without forcing the TA to infer the structure from notebook cells.