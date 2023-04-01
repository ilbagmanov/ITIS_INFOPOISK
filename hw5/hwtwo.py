import os
import re
import nltk

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from collections import defaultdict
nltk.download('stopwords')
stop_words = stopwords.words('russian') + stopwords.words('english')

def upload_tokens_to_file(content, path):
    file = open(path, "w", encoding="utf-8")
    file.write(content)
    file.close()

def upload_lemmas_to_file(lemmas, path):
    file = open(path, "w", encoding="utf-8")
    for k, v in lemmas.items():
        file.write(k + ": ")
        for word in v:
            file.write(word + " ")
        file.write("\n")
    file.close()

def get_text_from_file(path):
    f = open(path, encoding="utf-8")
    html_text = f.read()
    f.close()
    soup = BeautifulSoup(html_text, "lxml")
    return ' '.join(soup.stripped_strings)

def get_tokens(s):
    tknzr = RegexpTokenizer('[А-Яа-яёЁ]+')
    re.sub(r"[^А-Яа-яёЁ ]+[-'`][А-Яа-яёЁ]+"," ", s)
    words = tknzr.tokenize(s)
    result = []
    for word in words:
        word = word.lower()
        if (word not in stop_words):
            result.append(word)
    return result


def get_lemmas(tokens):
    pymorphy2_analyzer = MorphAnalyzer()
    lemmas = defaultdict(list)
    for token in tokens:
        lemma = pymorphy2_analyzer.parse(token)[0].normal_form
        lemmas[lemma].append(token)
    return lemmas

def prepare_folders():
    os.makedirs(os.path.dirname("токены_леммы/токены/"), exist_ok=True)
    os.makedirs(os.path.dirname("токены_леммы/леммы/"), exist_ok=True)

if __name__ == '__main__':
    prepare_folders()
    all_tokens = []
    for root, dirs, files in os.walk("Выкачка"):
        for file in files:
            index = file.split('.')[0]
            text = get_text_from_file(os.path.join(root, file))
            tokens = list(set(get_tokens(text)))
            lemmas = get_lemmas(tokens)
            upload_tokens_to_file('\n'.join(tokens), f"токены_леммы/токены/tokens_{index}.txt")
            upload_lemmas_to_file(lemmas, f"токены_леммы/леммы/lemmas_{index}.txt")
            all_tokens += tokens
    all_tokens = list(set(all_tokens))
    all_lemmas = get_lemmas(all_tokens)
    upload_tokens_to_file('\n'.join(all_tokens), f"токены_леммы/all_tokens.txt")
    upload_lemmas_to_file(all_lemmas, f"токены_леммы/all_lemmas.txt")