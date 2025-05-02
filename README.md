# AgentQL Conference Presenter Extractor

This Streamlit app uses the AgentQL API to extract structured presenter data from conference program URLs and allows downloading it as a CSV file.

## How to Run

### Locally

1. Clone this repo:
   ```
   git clone https://github.com/your-username/conference-presenter-extractor.git
   cd conference-presenter-extractor
   ```

2. Install requirements:
   ```
   pip install -r requirements.txt
   ```

3. Add your API key to `.streamlit/secrets.toml`:
   ```
   agentql_api_key = "your-api-key"
   ```

4. Run the app:
   ```
   streamlit run streamlit_app.py
   ```

### Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Visit [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub, select the repo, and deploy