from itertools import chain
import requests
from bs4 import BeautifulSoup as Soup


def print_results(target_language, file_name, words_list, sentences_list):

    # Printing translated words:
    file_name.write(f'\n\n{target_language} Translations:\n')
    print(f'\n{target_language} Translations:\n')
    for translated_word in words_list:
        output.write('\n' + translated_word)
        print(translated_word)

    # Printing Examples of sentences:
    file_name.write(f'\n\n{target_language} Examples:\n')
    print(f'\n{target_language} Examples:\n')
    for sentence in sentences_list:
        file_name.write('\n' + sentence)
        print(sentence)


print("Hello, you're welcome to the translator. Translator supports: ")

print("1. Arabic\n2. German\n3. English\n4. Spanish\n5. French\n6. Hebrew\n7. Japanese\n8. Dutch\n9. "
      "Polish\n10.Portuguese\n11. Romanian\n12. Russian\n13. Turkish")

languages = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'hebrew', 7: 'Japanese',
             8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian', 13: 'Turkish'}


key_sr = int(input('Type the number of your language: \n'))

key_tr = int(input("Type the number of a language you want to translate to or '0' to translate to all languages: \n"))

text = input('Type the word you want to translate:\n')

source_lang = languages[key_sr]

target_words = []
sentences = []

headers = {'User-Agent': 'Mozilla/5.0'}

output = open(f"{text}.txt", 'w', encoding='utf-8')

s = requests.Session()

if key_tr == 0:

    for value in languages.values():

        url = f"https://context.reverso.net/translation/{source_lang.lower()}-{value.lower()}/{text}"

        r = s.get(url, headers=headers)

        if r.status_code == 200:

            soup = Soup(r.content, 'html.parser')

            words_tr = soup.find_all('a', {"class": 'translation'})

            source_sentences = soup.find_all('div', {"class": "src ltr"})

            target_sentences = soup.find_all('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})

            for word in words_tr:
                target_words.append(word.get_text().strip())

            sentences = [sentence.get_text().strip() for sentence in
                         list(chain(*[sentence_pair for sentence_pair in zip(source_sentences, target_sentences)]))]

            print_results(value, output, target_words, sentences)

            target_words = []

else:

    url = f"https://context.reverso.net/translation/{source_lang.lower()}-{languages[key_tr].lower()}/{text}"

    r = s.get(url, headers=headers)

    if r.status_code == 200:

        soup = Soup(r.content, 'html.parser')

        words_tr = soup.find_all('a', {"class": 'translation'})

        source_sentences = soup.find_all('div', {"class": "src ltr"})

        target_sentences = soup.find_all('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})

        for word in words_tr:
            target_words.append(word.get_text().strip())

        sentences = [sentence.get_text().strip() for sentence in
                     list(chain(*[sentence_pair for sentence_pair in zip(source_sentences, target_sentences)]))]

        print_results(languages[key_tr], output, target_words, sentences)

output.close()
