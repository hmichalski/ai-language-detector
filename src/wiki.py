import requests
import wikipedia # type: ignore
from bs4 import BeautifulSoup # type: ignore

class Wikipedia:
    def languages(self):
        """
        Fetches a list of languages and their corresponding language codes from the
        Wikipedia page that lists all Wikipedias.

        :return: A list of dictionaries, where each dictionary contains:
                 - 'name': The name of the language (e.g., 'English'). 
                 - 'code': The language code used by Wikipedia (e.g., 'en').
        """
        
        url = "https://en.wikipedia.org/wiki/List_of_Wikipedias"
        response = requests.get(url)
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
                    'name': language_name,
                    'code': language_code
                })

        return languages

    def random_article(self, language_code):
        try: 
            wikipedia.set_lang(language_code)
            page_name = wikipedia.random(pages=1)
            page = wikipedia.page(page_name)
            return page.content
        except wikipedia.exceptions.WikipediaException as e:
            return f"An error occurred: {e}"
    
# Example usage
if __name__ == "__main__":
    scraper = Wikipedia()

    languages = scraper.languages()
    languages_codes = [lang['code'] for lang in languages]

    for l in languages:
        code = l['code']
        name = l['name']
        print(f'{name}, {code}')
        print("-" * 50)
        print(scraper.random_article(code)[:50])
        print("\n")