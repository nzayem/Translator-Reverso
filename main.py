from itertools import chain
import requests
from bs4 import BeautifulSoup as Soup

print("Hello, you're welcome to the translator. Translator supports: ")
print('''1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish''')

languages = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'hebrew', 7: 'Japanese',
             8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian', 13: 'Turkish'}


key_sr = int(input('Type the number of your language: \n'))

key_tr = int(input('Type the number of language you want to translate to: \n'))

text = input('Type the word you want to translate:\n')

print(f'You chose {languages[key_tr]} as the language to translate {text} to.')

source_lang = languages[key_sr]

target_lang = languages[key_tr]


headers = {'User-Agent': 'Mozilla/5.0'}

url = f"https://context.reverso.net/translation/{source_lang.lower()}-{target_lang.lower()}/{text}"

print(url)

r = requests.get(url, headers=headers)

target_words = []

sentences = []

if r.status_code == 200:

    soup = Soup(r.content, 'html.parser')

    words_tr = soup.find_all('a', {"class": 'translation'})

    source_sentences = soup.find_all('div', {"class": "src ltr"})

    target_sentences = soup.find_all('div', {"class": "trg ltr"})

    for word in words_tr:
        target_words.append(word.get_text().strip())

    sentences = [sentence.get_text().strip() for sentence in
                 list(chain(*[sentence_pair for sentence_pair in zip(source_sentences, target_sentences)]))]

else:

    print("Connection Error")

print(f"\n{target_lang.capitalize()} Translations:\n")


for word in target_words:

    print(word)

print(f'\n{target_lang.capitalize()} Examples:\n')

for sentence in sentences:

    print(sentence)
