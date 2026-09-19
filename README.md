# 📚 Live Research & Paper Aggregator

A real-time academic paper aggregator built with Python and Streamlit. This tool connects directly to the ArXiv API to fetch the latest research papers across various computer science domains, making it easy to skim abstracts, search for specific topics, and find highly relevant papers using a custom confidence scoring algorithm.

## ✨ Features
* **Live API Integration:** Fetches the most recent academic papers directly from ArXiv.
* **Category Filtering:** Easily toggle between Machine Learning, Data Structures & Algorithms, Artificial Intelligence, and Computer Vision.
* **Keyword Matching & Confidence Scoring:** Enter a search term to calculate a "Match %" based on keyword frequency in the paper's title and abstract.
* **Multi-Tier Sorting:** Automatically sorts results first by the highest confidence score, then by the most recent publication date.
* **Clean UI:** Reads easily with expandable cards containing authors, abstracts, and direct PDF links.

## 🛠️ Tech Stack
* **Frontend/Framework:** Streamlit
* **Backend Data Fetching:** Python `urllib` & `feedparser` (ArXiv Atom XML)
* **Environment Management:** `python-dotenv`
* **Language:** Python 3.12+
