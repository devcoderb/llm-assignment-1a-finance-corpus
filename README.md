# Assignment 1A — Continued Pretraining and QLoRA

Domain: **Indian Financial Markets and Digital Payments**

This repository contains the implementation for Assignment 1A covering:

- PDF text extraction and corpus cleaning
- Tokenization and packed dataset creation
- Continued Pretraining (CPT)
- Domain evaluation and perplexity comparison
- Instruction dataset generation
- QLoRA supervised fine-tuning
- Base vs CPT vs CPT+QLoRA evaluation

## Corpus

The source corpus contains 8 publicly available financial-domain documents from RBI, SEBI, and NPCI.

Source PDFs are stored under:

`data/corpus/v1/Finance/`

The notebook processes these files automatically using relative paths.

## Running

Open `Assignment-1a.ipynb` and execute the notebook cells in order.

Required Python packages are checked by the notebook and missing dependencies are installed when required.

## Generated Outputs

During execution, the notebook will create the required output directories and artifacts, including cleaned text, packed datasets, evaluation results, plots, and model outputs.

## Notes

The original PDFs under `data/corpus/v1/` are treated as the frozen source corpus and should not be modified during preprocessing.