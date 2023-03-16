import os
import re
import nltk

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from collections import defaultdict
nltk.download('stopwords')

DIRECTORY = "Выкачка"
stop_words = stopwords.words('russian') + stopwords.words('english')

def get_text_from_file(path):
    f = open(path, encoding="utf-8")
    html_text = f.read()
    f.close()
    soup = BeautifulSoup(html_text, "lxml")
    return ' '.join(soup.stripped_strings)

def get_tokens(s):
    tknzr = RegexpTokenizer('[А-Яа-яёЁ]+')
    re.sub(r"[^А-Яа-яёЁ ]+[-'`][А-Яа-яёЁ]+"," ", s)
    clean_words = tknzr.tokenize(s)
    clean_words = [w.lower() for w in clean_words if w != '' and w not in stop_words]
    return list(set(clean_words))


def get_lemmas(tokens):
    pymorphy2_analyzer = MorphAnalyzer()
    lemmas = defaultdict(list)
    for token in tokens:
        lemma = pymorphy2_analyzer.parse(token)[0].normal_form
        lemmas[lemma].append(token)
    return lemmas
    

def get_total_result():
    tokens = []
    for root, dirs, files in os.walk(DIRECTORY):
        for file in files:
            text = get_text_from_file(os.path.join(root, file))
            tokens += get_tokens(text)
    tokens = list(set(tokens))
    tokens_string = '\n'.join(tokens)
    path_result = f"Выкачка_очищенная_общая/tokens.txt"
    os.makedirs(os.path.dirname(path_result), exist_ok=True)
    with open(path_result, "w", encoding="utf-8") as file_result:
        file_result.write(tokens_string)
    lemmas_dict = get_lemmas(tokens)
    path_result = f"Выкачка_очищенная_общая/lemmas.txt"
    with open(path_result, "w", encoding="utf-8") as file_result:
        for k, v in lemmas_dict.items():
            file_result.write(k + ": ")
            for word in v:
                file_result.write(word + " ")
            file_result.write("\n")

if __name__ == '__main__':
    get_total_result()
    #get_every_file()