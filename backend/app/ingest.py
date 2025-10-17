import weaviate
import requests
from bs4 import BeautifulSoup

client = weaviate.Client("http://localhost:8080")

urls = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Natural_language_processing",
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No Title"
        paragraphs = [p.get_text().strip() for p in soup.find_all("p") if p.get_text().strip()]
        content = " ".join(paragraphs[:10])  # more text!

        client.data_object.create(
            {
                "title": title,
                "content": content,
                "url": url,
            },
            "Article"
        )

        print(f"✅ Added: {title} ({len(content)} characters)")

    except Exception as e:
        print(f"❌ Error with {url}: {e}")

print("🎉 Ingestion complete!")
