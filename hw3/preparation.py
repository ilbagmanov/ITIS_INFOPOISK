from collections import defaultdict
import os

DIRECTORY = 'clean'
LEMASS = 'lemmas'
TXT = '.txt'
UTF8 = "utf=8"
_UTF8 = "utf-8"
_N = '\n'

def get_inverted_index():
    term_documents_dict = defaultdict(list)
    idx = 0
    for root, dirs, files in os.walk(DIRECTORY):
        for file in files:
            if file.lower().endswith(TXT) and file.lower().startswith(LEMASS):
                idx += 1
                path_file = os.path.join(root, file)
                with open(path_file, encoding=UTF8) as f:
                    lemmas = list(map(lambda x: x.split(':')[0], f.readlines()))
                for lemma in lemmas:
                    term_documents_dict[lemma].append(idx)
    return term_documents_dict


if __name__ == '__main__':
    td_dict = get_inverted_index()
    with open('inverted_index.txt', 'w', encoding=_UTF8) as f:
        for k, v in td_dict.items():
            f.write(k + ' ' + ' '.join(map(str, v)) + _N)
    count_inverted_word = []
    for k, v in td_dict.items():
        count_inverted_word.append({"count": len(v), "inverted_array": v, "word": k})
    with open('inverted_index_2.txt', 'w', encoding=_UTF8) as f:
        for ciw in count_inverted_word:
            f.write(str(ciw) + _N)
