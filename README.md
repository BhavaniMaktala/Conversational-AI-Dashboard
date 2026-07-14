# Conversational BI Dashboard

A powerful business intelligence dashboard that allows users to upload CSV files and interact with their data using natural language queries, powered by Google's Gemini AI.

## Features

- 📤 **CSV Upload**: Easily upload any CSV file for analysis
- 💬 **Natural Language Queries**: Ask questions in plain English
- 📊 **Interactive Visualizations**: Generate pie charts, bar charts, line charts, and more
- 🤖 **AI-Powered Insights**: Get intelligent insights about your data
- 🔍 **Dynamic Filtering**: Filter and refine your data on the fly
- 📱 **Responsive Design**: Works on desktop and tablet devices

## Tech Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **AI/ML**: Google Gemini API
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/conversational-bi-dashboard.git
cd conversational-bi-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Google Gemini API key:
   - Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file and add:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```
   - Or use Streamlit secrets for deployment

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Upload Data**: Use the sidebar to upload your CSV file
2. **Ask Questions**: Type natural language queries in the chat interface
3. **View Visualizations**: See interactive charts generated from your queries
4. **Get Insights**: Review AI-generated insights about your data
5. **Filter Data**: Use quick filters or ask for specific conditions

### Example Queries

- "Show me a pie chart of sales by region"
- "Create a bar chart of product categories"
- "What's the average revenue per month?"
- "Filter data for East Coast region"
- "Show trends in customer satisfaction over time"
- "Compare sales across different product lines"

## Project Structure

```
conversational-bi-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── assets/
│   └── style.css         # Custom CSS styling
└── utils/
    ├── __init__.py
    ├── chart_generator.py # Plotly visualization logic
    ├── csv_processor.py   # Data manipulation and cleaning
    └── gemini_service.py  # AI integration

```
