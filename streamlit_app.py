import streamlit as st
import pandas as pd
import io
import requests
import os

API_KEY = st.secrets.get("agentql_api_key") or os.getenv("AGENTQL_API_KEY")

def run_agentql_query(url: str) -> list[dict]:
    API_URL = "https://api.agentql.com/v1/query-data"
    HEADERS = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "query": """
            {
                presenters[] {
                    Date (date of presentation MM/DD/YYYY format)
 		    Time (start time of presentation)
                    First_Presenter 
                    Title (title of the paper being presented)
                    Affiliation (school or company or lab affiliated with the first presenter)
		    Session (session ID or session name if available)
		    Location (room #, conference hall/floor, building, etc)
                }
            }
        """,
        "url": url,
        "params": {
            "wait_for": 2,
            "is_scroll_to_bottom_enabled": True,
            "mode": "fast",
            "is_screenshot_enabled": False
        }
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()

    result = response.json()
    return result.get("data", {}).get("presenters", [])

st.title("📄 AgentQL Conference Presenter Extractor")

# Step 1: Create form
with st.form("query_form"):
    url = st.text_input("Enter Conference Program URL")
    submitted = st.form_submit_button("Run Query")

# Step 2: Run extraction only on button press
if not API_KEY:
    st.error("❌ Missing API key. Please set AGENTQL_API_KEY in secrets.toml.")
elif submitted:
    with st.spinner("Querying AgentQL..."):
        try:
            data = run_agentql_query(url)
            df = pd.DataFrame(data).dropna(axis=1, how="all")

            if df.empty:
                st.warning("⚠️ No presenter data found.")
            else:
                # Store result in session_state to persist
                st.session_state["df"] = df
                st.success("✅ Data extracted!")

        except Exception as e:
            st.error(f"❌ AgentQL API error: {e}")

# Step 3: Display stored table if available
if "df" in st.session_state:
    st.dataframe(st.session_state["df"])

    csv_data = st.session_state["df"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name="conference_presenters.csv",
        mime="text/csv"
    )
