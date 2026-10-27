
# Ecommerce Revenue Intelligence Dashboard

An interactive dashboard for analyzing e-commerce sales data, monitoring revenue performance, and exploring business trends using Python, SQL, and data visualization.

## Project Overview

This project analyzes e-commerce transaction data to understand revenue, order volume, customer activity, product performance, and sales patterns.

The interactive dashboard was developed using Streamlit and Plotly, with SQL for data analysis and Pandas for data processing.

## Features

- Revenue, order, and customer KPI cards
- Country-level revenue analysis for the top 10 countries
- Monthly revenue trend visualization
- Top 10 products by revenue
- Sales analysis by day of the week
- Interactive country filters
- Data quality checks and cleaning scripts

## Tech Stack

- Python
- SQL (MySQL)
- Pandas
- Streamlit
- Plotly
- Microsoft Excel

## Project Structure

```text
Ecommerce-Revenue-Intelligence/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── python/
│   ├── clean_data.py
│   └── data_quality_check.py
├── sql/
│   └── sales_analysis.sql
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Run

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   streamlit run dashboard/app.py
   ```

5. Open the local URL shown in the terminal.

## Data

The project uses e-commerce transaction data. The original raw dataset is excluded from version control. Required processed data files should be placed in `data/processed/`.

## Purpose

The project demonstrates practical skills in SQL analysis, data cleaning, KPI development, interactive visualization, and business performance reporting.
