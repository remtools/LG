from googlesearch import search  # or use SerpAPI/Bing
from newspaper import Article    # or LangChain loader
from ast import literal_eval

def load_from_config(cfg=None):
    def web_search_tool(query=None, multi=False):
        """
        tool name: web_search

        Arguments:
          web_search(str): the search term

        Description:
          Searches Google and summarizes content from top results.
        """
        results = []
        urls = list(search(query, num_results=5))
        for url in urls:
            try:
                article = Article(url)
                article.download()
                article.parse()
                summary = article.text[:500]  # truncate
                results.append({
                    "title": article.title,
                    "url": url,
                    "snippet": summary
                })
                if not multi:
                    break
                if len(results) >= 3:
                    break
            except Exception as e:
                continue
        return results if multi else results[0] if results else {"error": "No result"}
    return web_search_tool
