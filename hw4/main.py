import re
import os
import config
from collections import defaultdict
from math import log
from config import PAGES_COUNT



# Ссылка на ресурс, где описаны формулы - https://sysblok.ru/glossary/kak-vychislit-tf-idf/

# TF - количество употребления ключевого термина по отношению ко всем словам в документе
def find_tf(terms_in_document):
    tf = defaultdict(float)
    for term in terms_in_document:
        tf[term] += 1
    for word, count in tf.items():
        tf[word] = count / len(terms_in_document)
    return tf

# IDF - log(общее количество документов / количество документов с вхождением слова)
def find_idf(all_terms, all_terms_group_by_document):
    idf = dict()
    for term in all_terms:
        doc_count = 0
        for terms in all_terms_group_by_document:
            if term in terms:
                doc_count += 1
        idf[term] = log(PAGES_COUNT / doc_count)
    return idf


# TF-IDF - TF * IDF
def find_tf_idf(tf, idf):
    tf_idf = dict()
    for term, tf_value in tf.items():
        tf_idf[term] = tf_value * idf[term]
    return tf_idf

def save(docs_tf_idf, docs_idf, type):
    for doc_num, tf_idf in enumerate(docs_tf_idf):
        num_file = f'{doc_num}'
        path = f'tf_idf/{type}/{type}_{num_file}.txt'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        file_result = open(path, "w", encoding="utf-8")
        for term, tf_idf_value in tf_idf.items():
            file_result.write(term + " " + str(docs_idf[term]) + " " + str(tf_idf_value))
            file_result.write("\n")
        file_result.close()


def analyse(type, path):
    all_terms = []
    all_terms_group_by_document = [None] * PAGES_COUNT
    docs_tf = [defaultdict(list) for _ in range(PAGES_COUNT)]
    for root, dirs, files in os.walk(path):
        for file in files:
            doc_num = int(re.findall(r'\d+', file)[0])
            path_file = os.path.join(root, file)
            with open(path_file, encoding="utf=8") as f:
                all_terms_group_by_document[doc_num] = (f.read().split('\n'))
                
                # Убрать, если нужно рассматривать не только слова в инфинитив форме
                all_terms_group_by_document[doc_num] = [term.split(':')[0] for term in all_terms_group_by_document[doc_num]]
                
                docs_tf[doc_num] = find_tf(all_terms_group_by_document[doc_num])
                all_terms += all_terms_group_by_document[doc_num]
    all_terms = list(set(all_terms))
    docs_idf = find_idf(all_terms, all_terms_group_by_document)
    docs_tf_idf = []
    for doc_tf in docs_tf:
        docs_tf_idf.append(find_tf_idf(doc_tf, docs_idf))
    save(docs_tf_idf, docs_idf, type)


if __name__ == '__main__':
    analyse(config.TOKENS_FILE_NAME, config.TOKENS_PATH)
    analyse(config.LEMMAS_FILE_NAME, config.LEMMAS_PATH)