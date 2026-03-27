# Endless Research Agent Web App

An autonomous AI research system that searches the real web, scrapes content, summarizes findings, and generates downloadable reports — built with a Material Design 3 UI.

## Features

- 🌐 **Real Web Search** — DuckDuckGo-powered live search
- 🕷️ **Web Scraping** — BeautifulSoup content extraction from real pages
- 📝 **Extractive Summarization** — Key sentence extraction from scraped content
- 📄 **Multi-Format Export** — Download reports as `.md`, `.pdf`, or `.docx`
- 🎨 **Material Design 3 UI** — Dark theme with Poppins font

## Project Structure

| File | Description |
|---|---|
| `index.html` | Frontend single-page application |
| `styles.css` | Material Design 3 styling (Poppins) |
| `script.js` | Frontend logic, fetch calls, export handlers |
| `main.py` | FastAPI backend server |
| `researcher.py` | Web search + scraping + summarization logic |
| `requirements.txt` | Python dependencies |

## Setup & Installation

### 1. Install Python dependencies (first time only)

```powershell
& "C:/Users/PRAVEEN PRABAKARN/AppData/Local/Programs/Python/Python313/python.exe" -m pip install -r requirements.txt
```

## Running the Application

You need **two terminals** open in the project folder.

### Terminal 1 — Start the Backend (FastAPI)

```powershell
cd "C:\Users\PRAVEEN PRABAKARN\Documents\Endless_Research_Agent_Web_App"
& "C:/Users/PRAVEEN PRABAKARN/AppData/Local/Programs/Python/Python313/python.exe" -m uvicorn main:app --reload --port 8000
```

> The backend runs on **http://localhost:8000** and handles all web searching and scraping.

### Terminal 2 — Start the Frontend (UI)

```powershell
cd "C:\Users\PRAVEEN PRABAKARN\Documents\Endless_Research_Agent_Web_App"
& "C:/Users/PRAVEEN PRABAKARN/AppData/Local/Programs/Python/Python313/python.exe" -m http.server 3000
```

> The frontend runs on **http://localhost:3000**.

### 3. Open the App in Browser

```
http://localhost:3000
```

## How to Use

1. Enter a research topic in the **Research Topic** field
2. Select your data sources (DuckDuckGo, Wikipedia, etc.)
3. Adjust the number of pages to analyse using the slider
4. Click **Start Autonomous Research**
5. Watch the Agent Console stream real-time results
6. Download the generated report as **Markdown**, **PDF**, or **Word**

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, Vanilla CSS (MD3), JavaScript |
| Backend | Python 3.13, FastAPI, Uvicorn |
| Search | `ddgs` (DuckDuckGo Search) |
| Scraping | `requests`, `BeautifulSoup4` |
| Export | jsPDF, docx.js, FileSaver.js |
| Font | Poppins (Google Fonts) |

## Roadmap

| Version | Status | Description |
|---|---|---|
| v1.0 | ✅ Completed | Core engine — search, scrape, summarize, export |
| v2.0 | 🔧 In Progress | LLM-powered summarization, knowledge graph |
| v3.0 | 📅 Upcoming | Real-time streaming UI, saved sessions |
| v4.0 | 📅 Upcoming | Multi-agent mode with fact-checking |
| v5.0 | 📅 Upcoming | SaaS platform with API access |
