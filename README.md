# SAM AI

This is an Agentic AI project built with Python for Software Asset Management (SAM) of Red Hat licenses in virtualized environments.

## Description

SAM AI is a tool that automates the analysis of Red Hat Enterprise Linux (RHEL) and Virtual Data Center (VDC) license entitlements in VMware virtualized infrastructures. The system processes Excel-based VM inventory data, calculates deterministic license requirements based on Red Hat licensing rules, and leverages OpenAI's GPT models to generate intelligent recommendations for license optimization, anomaly detection, and compliance adjustments.

Key features:
- Automated license calculation for RHEL and VDC subscriptions
- Cluster-based analysis respecting VDC atomicity rules
- AI-powered recommendations for cost optimization and compliance
- JSON output format for integration with other SAM tools

## Requirements

- Python 3.x
- pandas
- numpy
- openai
- python-dotenv
- openpyxl (for Excel reading)

## Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables: Create a `.env` file with your OpenAI API key and model (e.g., `API_KEY=your_key`, `MODEL=gpt-4`)

## Usage

1. Prepare your VM inventory data in an Excel file named `input.xlsx` with sheets:
   - `vInfo`: VM information including GuestOS and Cluster
   - `vHost`: Host information including Cluster and Host names

2. Run the main script: `python main.py`

The tool will output JSON recommendations for license adjustments, anomalies, and optimizations.