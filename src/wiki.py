import requests
from bs4 import BeautifulSoup

class WikipediaScraper:
    def __init__(self, url="https://en.wikipedia.org/wiki/List_of_Wikipedias"):
        self.url = url

    def fetch_wikipedias(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve page. Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})
        rows = table.find_all('tr')[1:]  # Skip the header row

        wikipedias = []

        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 0:
                language_name = columns[1].text.strip()  # Column for language name
                language_code = columns[3].text.strip()  # Column for language code

                wikipedias.append({
                    'language_name': language_name,
                    'language_code': language_code
                })

        return wikipedias

# Example usage
if __name__ == "__main__":
    scraper = WikipediaScraper()
    wikipedias = scraper.fetch_wikipedias()

    # Every language_code.wikipedia.org has a page
    for wikipedia in wikipedias:
        print(f"{wikipedia['language_code']}.wikipedia.org")