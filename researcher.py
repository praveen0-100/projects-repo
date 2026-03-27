import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import re


class Researcher:
    def __init__(self):
        self.ddgs = DDGS()

    # ── Search ──────────────────────────────────────────────────────────────────
    def search(self, query: str, max_results: int = 6):
        """Return a list of {title, href, body} dicts from DuckDuckGo."""
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            return results
        except Exception as e:
            print(f"[search error] {e}")
            return []

    # ── Scrape ──────────────────────────────────────────────────────────────────
    def scrape(self, url: str, max_chars: int = 6000) -> str:
        """Download a URL and return clean readable text (up to max_chars)."""
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
            )
        }
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            return f"[Could not fetch page: {e}]"

        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove junk tags
        for tag in soup(["script", "style", "nav", "footer",
                         "header", "aside", "form", "iframe"]):
            tag.decompose()

        # Prefer <article> or <main>, fall back to <body>
        body = (soup.find("article") or
                soup.find("main") or
                soup.find("body"))
        if not body:
            return "[No parseable content found]"

        # Collect non-empty paragraphs
        paragraphs = []
        for elem in body.find_all(["p", "h1", "h2", "h3", "li"]):
            text = elem.get_text(" ", strip=True)
            if len(text) > 40:
                paragraphs.append(text)

        full_text = "\n\n".join(paragraphs)
        # Collapse excessive whitespace
        full_text = re.sub(r'\n{3,}', '\n\n', full_text).strip()
        return full_text[:max_chars] if full_text else "[No readable content]"

    # ── Summarise ───────────────────────────────────────────────────────────────
    def summarize(self, text: str, sentences: int = 5) -> str:
        """Extractive summarizer: pick the best sentences by length heuristic."""
        if not text or text.startswith("["):
            return text
        all_sentences = re.split(r'(?<=[.!?])\s+', text)
        # Score: longer sentences (up to 200 chars) without too many numbers
        scored = [
            (s, min(len(s), 200) - s.count('%') - s.count('©'))
            for s in all_sentences
            if 30 < len(s) < 400
        ]
        scored.sort(key=lambda x: -x[1])
        top = [s for s, _ in scored[:sentences]]
        return " ".join(top) if top else text[:500]

    # ── Main entry point ────────────────────────────────────────────────────────
    def research(self, topic: str, sources: list, max_results: int = 5):
        """
        Search → scrape → summarise.
        Returns a list of result dicts ready for the frontend.
        """
        query = topic
        search_results = self.search(query, max_results=max_results)

        output = []
        for r in search_results:
            url = r.get("href", "")
            title = r.get("title", url)
            snippet = r.get("body", "")

            # Determine which source bucket this falls into
            source = "Web"
            if "wikipedia.org" in url:
                source = "Wikipedia"
            elif "arxiv.org" in url:
                source = "ArXiv"
            elif "news" in url or "bbc" in url or "reuters" in url or "cnn" in url:
                source = "News"
            elif "duckduck" in url:
                source = "DuckDuckGo"

            # Only include if the source is selected by the user
            # (If sources list is empty we include everything)
            if sources and source not in sources:
                source = "DuckDuckGo"  # default bucket for general web

            raw_content = self.scrape(url)
            summary = self.summarize(raw_content, sentences=5)

            output.append({
                "source": source,
                "title": title,
                "link": url,
                "snippet": snippet,
                "content": raw_content,   # full scraped text
                "summary": summary,       # short extractive summary
            })

        return output
