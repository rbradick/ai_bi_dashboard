# AI Business Intelligence Dashboard

This Streamlit app allows you to upload a CSV, Excel, or TXT file and get automatic business insights powered by OpenAI.

## Features
- Upload tabular data for instant analysis
- Automatically removes ID columns
- Parses date/time fields
- Identifies key numeric and categorical dimensions
- Generates line and bar charts
- Uses GPT-4o for AI-generated business insights

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Add your OpenAI API key:
Create a `.streamlit/secrets.toml` file with:
```
[OPENAI]
OPENAI_API_KEY = "your-api-key-here"
```

3. Run the app:
```bash
streamlit run updated_app.py
```
