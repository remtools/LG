import requests
from bs4 import BeautifulSoup
from googlesearch import search

def load_from_config(cfg=None):
    def web_search_tool(query=None, multi=False):
        """
        tool name: web_search

        Arguments:
            query (str): The search query.
            multi (bool): Optional. If True, returns summaries from multiple sources.

        Description:
            Performs a Google search and fetches readable content from the top result(s).
            If multi=True, returns up to 3 page summaries.
        """
        try:
            print(f"🔎 Searching Google for: {query}")
            urls = list(search(query, num_results=5))
            print("🔎 Found URLs:", urls)

            if not urls:
                return "No search results found."

            results = []

            for url in urls:
                try:
                    print(f"🌐 Fetching: {url}")
                    r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                    soup = BeautifulSoup(r.text, "html.parser")
                    title = soup.title.string.strip() if soup.title else "Untitled"
                    p = soup.find("p")
                    snippet = p.get_text(strip=True) if p else "No readable content found."
                    results.append(f"🔗 {title} — {url}\n{snippet}")
                except Exception as e:
                    print(f"⚠️ Skipped {url}: {e}")
                    continue

                if not multi and results:
                    return results[0]

                if multi and len(results) >= 3:
                    break

            return "\n\n".join(results) if results else "No readable content could be extracted."

        except Exception as e:
            return f"Search error: {e}"

    return web_search_tool
