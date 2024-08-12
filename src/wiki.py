import requests
from bs4 import BeautifulSoup

class WikipediaScraper:
    def __init__(self, url="https://en.wikipedia.org/wiki/List_of_Wikipedias"):
        self.url = url

    def fetch_wiki_languages(self):
        """
        Fetches a list of languages and their corresponding language codes from the
        Wikipedia page that lists all Wikipedias.

        :return: A list of dictionaries, where each dictionary contains:
                 - 'language_name': The name of the language (e.g., 'English').
                 - 'language_code': The language code used by Wikipedia (e.g., 'en').
        """
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve page. Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})
        rows = table.find_all('tr')[1:]  # Skip the header row

        languages = []

        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 0:
                language_name = columns[1].text.strip()  # Column for language name
                language_code = columns[3].text.strip()  # Column for language code

                languages.append({
                    'language_name': language_name,
                    'language_code': language_code
                })

        return languages
    
    def fetch_random_article(self, language_code):
        """
        Fetches a random Wikipedia article in the specified language.

        :param language_code: The language code (e.g., 'en', 'de', 'ty', 'pi', 'gcr').
        :return: URL of the random Wikipedia article.
        """
        url = f"https://{language_code}.wikipedia.org/wiki/Special:Random"
        response = requests.get(url)
    
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve article. Status code: {response.status_code}")
        
        return response.url
        
# Example usage
if __name__ == "__main__":
    scraper = WikipediaScraper()
    languages = scraper.fetch_wiki_languages()

    # Print the list of languages fetched
    for language in languages:
        print(language)

    # Fetch and print a random article for each language code
    print("\nFetching random articles for each language:")
    for language in languages:
        lang_code = language['language_code']
        random_article_url = scraper.fetch_random_article(lang_code)
        print(f"Random article URL in {lang_code}: {random_article_url}")