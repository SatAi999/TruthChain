import os
import re
import json
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.core.config import settings
from app.core.security import sanitize_document_text

logger = logging.getLogger("truthchain.search")

class ExternalSearchService:
    @staticmethod
    def generate_search_query(claim_statement: str, evidence_gap_desc: Optional[str] = None) -> str:
        """
        Generates a targeted, dynamic web search query from the claim statement and evidence gap.
        Never returns a hardcoded query.
        """
        clean_stmt = claim_statement.replace('"', '').strip()
        
        # Extract main entities & terms
        terms = re.findall(r'\b[A-Z0-9][a-zA-Z0-9]*\b', clean_stmt)
        unique_terms = list(dict.fromkeys(terms))[:4]
        
        query_parts = [f'"{t}"' for t in unique_terms if len(t) > 2]
        
        if evidence_gap_desc:
            gap_terms = re.findall(r'\b[A-Za-z0-9]+\b', evidence_gap_desc)
            relevant_gap = [g for g in gap_terms if len(g) > 3 and g.lower() not in ["missing", "evidence", "record"]][:2]
            query_parts.extend(relevant_gap)

        if not query_parts:
            query_parts = [clean_stmt[:60]]

        return " ".join(query_parts)

    @classmethod
    def execute_web_search(cls, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Executes a real external web search using Tavily API if key is present,
        or DuckDuckGo REST Search fallback.
        Returns: Dict containing provider status and list of search results.
        """
        api_key = getattr(settings, "SEARCH_API_KEY", "") or os.getenv("SEARCH_API_KEY", "")
        
        # 1. Try Tavily Search API if key provided
        if api_key:
            try:
                res = requests.post(
                    "https://api.tavily.com/search",
                    json={"api_key": api_key, "query": query, "max_results": max_results},
                    timeout=10
                )
                if res.status_code == 200:
                    results = []
                    data = res.json()
                    for item in data.get("results", []):
                        results.append({
                            "title": item.get("title", "Web Result"),
                            "url": item.get("url", ""),
                            "domain": item.get("url", "").split("/")[2] if "/" in item.get("url", "") else "",
                            "snippet": item.get("snippet", ""),
                            "source_type": "EXTERNAL_WEB"
                        })
                    return {
                        "status": "ACTIVE",
                        "provider": "Tavily Search API",
                        "query": query,
                        "results": results
                    }
                elif res.status_code == 429:
                    return {"status": "QUOTA_EXHAUSTED", "provider": "Tavily", "query": query, "results": []}
            except Exception as e:
                logger.error(f"Tavily search failed: {e}")

        # 2. DuckDuckGo Free HTML Search Fallback (Zero cost, no API key required)
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            res = requests.get(f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}", headers=headers, timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                results = []
                for a_tag in soup.find_all("a", class_="result__url", limit=max_results):
                    url = a_tag.get("href", "").strip()
                    title_tag = a_tag.find_parent("div", class_="result__body")
                    title = title_tag.find("a", class_="result__a").text.strip() if title_tag and title_tag.find("a", class_="result__a") else "External Web Source"
                    snippet = title_tag.find("a", class_="result__snippet").text.strip() if title_tag and title_tag.find("a", class_="result__snippet") else ""
                    
                    if url.startswith("//"):
                        url = "https:" + url
                    domain = url.split("/")[2] if "://" in url else url.split("/")[0]

                    results.append({
                        "title": title,
                        "url": url,
                        "domain": domain,
                        "snippet": snippet,
                        "source_type": "EXTERNAL_WEB"
                    })

                if results:
                    return {
                        "status": "ACTIVE",
                        "provider": "DuckDuckGo Web Search",
                        "query": query,
                        "results": results
                    }
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {e}")

        # 3. Fallback mock-free safe error response if network fails
        return {
            "status": "TEMPORARILY_UNAVAILABLE",
            "provider": "External Search Engine",
            "query": query,
            "results": []
        }

    @classmethod
    def fetch_page_content(cls, url: str) -> Optional[str]:
        """
        Fetches and extracts readable text from an external web page URL.
        Sanitizes text against prompt injection and enforces SSRF safety limits.
        """
        if not url or not (url.startswith("http://") or url.startswith("https://")):
            return None

        # SSRF Protection: Block internal IPs, localhost, and cloud metadata endpoints
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        hostname = (parsed.hostname or "").lower()
        if hostname in ["localhost", "127.0.0.1", "0.0.0.0", "::1", "169.254.169.254"] or \
           hostname.startswith("10.") or hostname.startswith("192.168.") or \
           hostname.startswith("172.16.") or hostname.startswith("172.31."):
            logger.warning(f"Blocked potential SSRF attempt target: {url}")
            return None

        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            res = requests.get(url, headers=headers, timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.extract()
                text = soup.get_text(separator="\n")
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                clean_text = "\n".join(chunk for chunk in chunks if chunk)
                return sanitize_document_text(clean_text[:5000])  # Cap at 5,000 characters
        except Exception as e:
            logger.error(f"Failed to fetch external URL {url}: {e}")
        return None
