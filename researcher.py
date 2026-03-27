import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import re

class Researcher:
    def __init__(self):
        self.ddgs = DDGS()

    def search_web(self, query, max_results=5):
        """Search DuckDuckGo and return a list of results."""
        try:
            results = [r for r in self.ddgs.text(query, max_results=max_results)]
            return results
        except Exception as e:
            print(f"Error searching DuckDuckGo: {e}")
            return []

    def scrape_url(self, url):
        """Scrape the content of a URL and return cleaned text."""
        try:
            response = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })
            if response.status_code != 200:
                return f"Error: Status code {response.status_code}"
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            return f"Error scraping {url}: {e}"

    def summarize(self, text, max_sentences=3):
        """A simple extractive summarizer that picks key sentences."""
        if not text:
            return ""
        
        # Split into sentences (simple regex)
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        if not sentences:
            return "No significant content found."
        
        # In a real app, use an LLM here. 
        # For now, let's take the first max_sentences for "overview"
        return " ".join(sentences[:max_sentences])

    def research_topic(self, topic, sources=["DuckDuckGo", "Wikipedia"]):
        """Orchestrate search, scrape, and summarize."""
        all_results = []
        
        if "DuckDuckGo" in sources:
            web_results = self.search_web(topic, max_results=4)
            for res in web_results:
                content = self.scrape_url(res['href'])
                summary = self.summarize(content)
                all_results.append({
                    "source": "DuckDuckGo",
                    "title": res['title'],
                    "link": res['href'],
                    "snippet": res['body'],
                    "summary": summary
                })
        
        if "Wikipedia" in sources:
            # Simple wiki search
            wiki_query = f"{topic} site:wikipedia.org"
            wiki_results = self.search_web(wiki_query, max_results=1)
            for res in wiki_results:
                content = self.scrape_url(res['href'])
                summary = self.summarize(content, max_sentences=5)
                all_results.append({
                    "source": "Wikipedia",
                    "title": res['title'],
                    "link": res['href'],
                    "snippet": res['body'],
                    "summary": summary
                })
        
        return all_results

if __name__ == "__main__":
    # Small test
    r = Researcher()
    print("Testing search and scrape...")
    res = r.research_topic("AI in Healthcare", sources=["DuckDuckGo"])
    for item in res:
        print(f"Title: {item['title']}\nSummary: {item['summary']}\n")
