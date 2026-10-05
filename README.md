# Evidence Prompt Generation

A configurable prompt-generation pipeline for building **text-rich Evidence Records image datasets**.

This project generates structured document specifications from predefined taxonomies, document skeletons, and controlled visual factors, then uses an LLM through an OpenAI-compatible API to expand them into detailed image-generation prompts.

The current version focuses on **Evidence Records**, including medical records, academic records, legal/dispute records, inspection reports, logistics records, and institutional/employment records.

## Motivation

The goal is to support large-scale construction of AI-generated text-rich document image datasets without manually writing thousands of prompts.

```text
Human-defined taxonomy and document structure
        ↓
Structured specification
        ↓
LLM expansion
        ↓
Final image-generation prompt
```

Core principle:

> **Human controls what should appear; the LLM controls how to describe it.**

This keeps the generation process controllable, reproducible, and diverse.

## Current Taxonomy

The current Evidence Records taxonomy contains **6 major categories and 27 document types**.

### Medical & Health Records
- Laboratory Test Report
- Medical Examination Report
- Diagnostic Report
- Imaging Report

### Academic Records
- Academic Transcript
- Examination Result Report
- Grade Report
- Credit Record

### Legal & Dispute Records
- Lawyer Letter
- Legal Opinion
- Dispute Record
- Case Fact Record

### Inspection & Verification Records
- Product Quality Inspection Report
- Food Inspection Report
- Environmental Test Report
- Equipment Inspection Report
- Appraisal Report

### Logistics & Delivery Records
- Shipping Label
- Waybill
- Delivery Record
- Proof of Delivery
- Logistics Tracking Record

### Institutional & Employment Records
- Attendance Record
- Performance Report
- Work Incident Record
- Meeting Record
- Employment Record

## Project Structure

```text
evidence_prompt_generation/
├── taxonomy.json
├── skeletons.json
├── factors.json
├── document_constraints.json
├── generate_specs.py
├── expand_prompt.py
├── generate_prompts.py
├── test_api.py
├── run_generate_prompts.bat
├── requirements.txt
├── .env.example
├── .gitignore
└── outputs/
```

## How It Works

### `taxonomy.json`
Defines the major categories and document types.

### `skeletons.json`
Defines the basic structure of each document type:
- overall description
- layout structure
- candidate image-text fields

### `factors.json`
Defines global variation factors, such as:
- language
- orientation
- text density
- capture style
- layout style
- visual condition
- document theme
- background

### `document_constraints.json`
Restricts factor choices for each document type so that unrealistic combinations are avoided.

For example, a lawyer letter can use paragraph-based or section-based layouts, while a shipping label is limited to compact label or form-like layouts.

### `generate_specs.py`
Generates structured specifications by:
1. randomly selecting one document type from the global pool;
2. loading its skeleton;
3. sampling valid factors;
4. sampling a subset of image-text fields.

All 27 document subcategories are sampled with equal probability.

### `expand_prompt.py`
Expands a structured specification into one detailed image-generation prompt through an OpenAI-compatible API.

Prompt language is randomly selected:
- Chinese: 50%
- English: 50%

Current target lengths:
- Chinese: approximately **450–550 Chinese characters**
- English: approximately **180–220 words**

### `generate_prompts.py`
Main controller for single or batch generation.

```text
generate_specs.py
        ↓
expand_prompt.py
        ↓
final prompt
```

### `run_generate_prompts.bat`
Windows launcher for interactive generation without manually typing the full Python command.

## Installation

```bash
pip install -r requirements.txt
```

Minimal dependencies:

```text
openai
python-dotenv
```

## API Configuration

Create a local `.env` file:

```text
API_KEY=your_api_key
BASE_URL=your_api_base_url
MODEL_NAME=your_model_name
```

Do **not** upload `.env` to GitHub.

## Usage

Generate one prompt:

```bash
python generate_prompts.py single
```

Generate multiple prompts:

```bash
python generate_prompts.py batch --count 10 --output prompts_10.txt
```

Optional delay between API calls:

```bash
python generate_prompts.py batch --count 100 --output prompts_100.txt --sleep 1
```

On Windows, you can also run:

```text
run_generate_prompts.bat
```

## Output

The final output is a plain `.txt` file.

Only the final prompts are saved. Structured specifications are used internally and are not written to the final output.

Each prompt is separated by a blank line.

## Design Principles

### Controlled variation
Randomness is restricted to predefined valid pools instead of unrestricted combinations.

### Text-rich focus
Each document skeleton contains multiple structured text fields, and most fields are retained during sampling.

### Reproducible structure
Taxonomy, skeletons, factors, and constraints are stored independently as configuration files.

### LLM as an expander, not a planner
The LLM does not decide the taxonomy or core document structure. It only turns a structured specification into a natural, detailed prompt.

### Dataset-bias awareness
Generation instructions avoid repeatedly inserting visible markers such as:

```text
sample
fictional
synthetic
demo
example
```

because repeated markers may introduce unwanted shortcuts into a downstream detector.

## Current Status

Implemented:
- 6 major Evidence Records categories
- 27 document types
- structured document skeletons
- document-specific factor constraints
- equal-probability document-type sampling
- structured specification generation
- OpenAI-compatible API integration
- Chinese / English prompt generation
- single and batch generation
- TXT output
- Windows BAT launcher
- configuration validation

## Possible Next Steps

- prompt-length validation
- duplicate detection
- semantic similarity filtering
- forbidden-word filtering
- prompt quality scoring
- generation statistics
- downstream image-generation API integration
- dataset metadata logging
- large-scale batch generation and review

## Research Context

This repository is part of an ongoing research workflow for constructing and studying **text-rich AI-generated document images**.

The current code should be treated as a research prototype rather than a finished production system.
