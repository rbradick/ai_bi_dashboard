
import streamlit as st
import pandas as pd
import plotly.express as px
import openai
import os

# 1️⃣ PAGE CONFIG
st.set_page_config(page_title="AI Business Intelligence Dashboard", layout="wide")
st.title("📊 AI Business Intelligence Dashboard")
st.write("Upload your CSV, Excel, or TXT file. This dashboard will analyze it and provide business insights automatically.")

# 2️⃣ SECURE API KEY
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.warning("⚠️ OpenAI API key not found. Please add it to `.streamlit/secrets.toml` or your environment.")

# 3️⃣ FILE UPLOADER
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.txt'):
            df = pd.read_csv(uploaded_file, delimiter="\t")
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type!")
            st.stop()

        st.success(f"✅ Uploaded: `{uploaded_file.name}`")
        st.subheader("Data Preview")
        st.dataframe(df.head())

        # Drop ID-like columns
        id_like_cols = [col for col in df.columns if 'id' in col.lower() or df[col].nunique() == len(df)]
        df = df.drop(columns=id_like_cols, errors='ignore')

        # Parse datetime columns
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # 4️⃣ METRICS
        st.subheader("Key Metrics")
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if numeric_cols:
            for col in numeric_cols:
                st.write(f"**Metrics for `{col}`**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", f"{df[col].sum():,.2f}")
                with col2:
                    st.metric("Average", f"{df[col].mean():,.2f}")
                with col3:
                    st.metric("Max", f"{df[col].max():,.2f}")
        else:
            st.warning("No numeric columns found.")

        # 5️⃣ CHARTS
        st.subheader("Visual Trends")
        time_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
        cat_cols = df.select_dtypes(include='object').columns.tolist()

        time_col = time_cols[0] if time_cols else None
        cat_col = cat_cols[0] if cat_cols else None

        if numeric_cols:
            target_num_col = numeric_cols[0]
            if time_col:
                df_sorted = df.dropna(subset=[time_col]).sort_values(time_col)
                fig1 = px.line(df_sorted, x=time_col, y=target_num_col, title=f"{target_num_col} Over Time")
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No time column for line chart.")

            if cat_col:
                top_cats = df.groupby(cat_col)[target_num_col].sum().sort_values(ascending=False).head(10)
                fig2 = px.bar(top_cats, x=top_cats.index, y=top_cats.values, title=f"Top {cat_col} by {target_num_col}")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No categorical column for bar chart.")

            # 6️⃣ AI INSIGHTS
            st.subheader("📌 AI-Generated Insights")
            if openai.api_key:
                with st.spinner("Generating insights with OpenAI..."):
                    prompt = f"""
You are a senior data analyst. The dataset below has been preprocessed to remove IDs and irrelevant fields.
Your task is to provide business insights and identify key drivers of performance.

Summary Statistics:
- Most important numeric column: `{target_num_col}` with total={df[target_num_col].sum():,.2f}, avg={df[target_num_col].mean():,.2f}
"""
                    if cat_col:
                        top_val = df.groupby(cat_col)[target_num_col].sum().idxmax()
                        prompt += f"\n- Top `{cat_col}` by `{target_num_col}`: `{top_val}`"
                    if time_col:
                        prompt += f"\n- Time trend available on `{time_col}`"

                    prompt += "\n\nPlease generate a concise analysis highlighting patterns, outliers, and opportunities."

                    response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a business intelligence assistant."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    st.write(response.choices[0].message.content)
            else:
                st.info("Add an OpenAI API key to enable AI insights.")
        else:
            st.warning("No numeric columns for charts or AI insights.")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👈 Upload a file to begin.")
