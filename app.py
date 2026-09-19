import streamlit as st
import os
from dotenv import load_dotenv
from arxiv_fetcher import fetch_latest_papers

# Load environment variables
load_dotenv()
app_name = os.getenv("APP_NAME", "Paper Aggregator")

# Configure page
st.set_page_config(page_title=app_name, page_icon="📚", layout="wide")

st.title("📚 Live Research & Paper Aggregator")
st.markdown("Skim the latest academic abstracts before class.")

# Sidebar Filters
st.sidebar.header("Search Parameters")
category_names = {
    "Machine Learning": "cat:cs.LG",
    "Data Structures & Algorithms": "cat:cs.DS",
    "Artificial Intelligence": "cat:cs.AI",
    "Computer Vision": "cat:cs.CV"
}
selected_cat = st.sidebar.selectbox("Select Focus Area", list(category_names.keys()))

# Text input for keyword searching
search_text = st.sidebar.text_input("Search Topics / Keywords", placeholder="e.g., neural networks")

# Number of papers to fetch
paper_count = st.sidebar.slider("Number of papers to fetch", 10, 50, 20)

def calculate_confidence(paper, search_query):
    """Calculates a match confidence score based on keyword frequency."""
    if not search_query:
        return 0
        
    words = search_query.lower().split()
    score = 0
    title_lower = paper.title.lower()
    summary_lower = paper.summary.lower()
    
    for word in words:
        # Title matches hold higher weight (3 points) than abstract matches (1 point)
        score += title_lower.count(word) * 3
        score += summary_lower.count(word) * 1
        
    # Scale the raw score for UI display and cap it at 100%
    return min(score * 15, 100)

# Fetch Data
with st.spinner('Fetching latest papers from ArXiv...'):
    papers = fetch_latest_papers(category=category_names[selected_cat], search_text=search_text, max_results=paper_count)

# Render UI
if papers:
    # 1. Calculate scores and attach them to the paper objects
    scored_papers = []
    for paper in papers:
        score = calculate_confidence(paper, search_text)
        scored_papers.append((score, paper))
        
    # 2. Multi-tier sort: Primary = Confidence Score (Desc), Secondary = Date (Desc)
    scored_papers.sort(key=lambda x: (x[0], x[1].published), reverse=True)
    
    for score, paper in scored_papers:
        title = paper.title.replace('\n', ' ')
        authors = ", ".join(author.name for author in paper.authors)
        summary = paper.summary.replace('\n', ' ')
        published_date = paper.published[:10]
        pdf_link = paper.link
        
        # 3. Format the expander header based on whether a search is active
        if search_text:
            badge = f"🔥 {score}% Match" if score > 0 else "0% Match"
            header = f"[{badge}] **{title}** — *{published_date}*"
        else:
            header = f"**{title}** — *{published_date}*"
        
        with st.expander(header):
            st.markdown(f"**Authors:** {authors}")
            st.markdown(f"**Abstract:** {summary}")
            st.markdown(f"[🔗 View PDF / Read More]({pdf_link})")
else:
    st.error("Failed to retrieve papers. Check your connection or try again.")