# AI Business Intelligence Dashboard

This app allows you to upload a dataset (CSV, Excel, or TXT) and automatically generates:
- Key metrics and trends
- Interactive charts
- AI-generated business insights using OpenAI's GPT model

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Setup

Ensure your OpenAI API key is available either via environment variable `OPENAI_API_KEY` or `.streamlit/secrets.toml`:

```toml
[OPENAI]
OPENAI_API_KEY="your-key-here"
```

## Features
- Auto-preprocessing of uploaded data
- Dynamic metric and chart rendering
- AI-generated analysis with enhanced prompt context
- More visualization types and downloadable insights
