from collections import defaultdict
import os

DIRECTORY = 'Выкачка_очищенная'

def get_lemmas(text):
    return [token.split(':')[0] for token in text.split()]

def get_inverted_index():
    term_documents_dict = defaultdict(list)
    idx = 0
    for root, dirs, files in os.walk(DIRECTORY):
        print(files)
        for file in files:
            if file.lower().endswith('.txt') and file.lower().startswith('lemmas'):
                idx += 1
                with open(os.path.join(root, file), encoding='utf-8') as f:
                    lemmas = get_lemmas(f.read())
                for lemma in lemmas:
                    term_documents_dict[lemma].append(idx)
    return term_documents_dict

if __name__ == '__main__':
    inverted_index = get_inverted_index()
    with open('inverted_index.txt', 'w', encoding='utf-8') as f:
        for term, docs in inverted_index.items():
            f.write(f"{term} {' '.join(map(str, docs))}\n")
    inverted_index_info = [{'count': len(docs), 'inverted_array': docs, 'word': term} for term, docs in inverted_index.items()]
    with open('inverted_index_2.txt', 'w', encoding='utf-8') as f:
        for term_info in inverted_index_info:
            f.write(str(term_info) + '\n')
