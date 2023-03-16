import argparse
import re
import sys

from nltk import RegexpTokenizer
from pymorphy2 import MorphAnalyzer
from inverted_index import get_inverted_index

OPERATORS = ['&', '|']
ALL_DOCUMENTS = set(range(100))
PRIORITY = {'&': 2, '|': 1}
REGEX_TOKENIZER = RegexpTokenizer(r'[А-Яа-яёЁ&(\|)~\)\(]+')
PYMORPHY2_ANALYZER = MorphAnalyzer()

inverted_index = get_inverted_index()


def get_index(word):
    if word[0] == '~':
        try:
            indices = set(inverted_index[word[1:]])
            return ALL_DOCUMENTS - indices
        except KeyError:
            return set()
    else:
        try:
            index = inverted_index[word]
            return set(index)
        except KeyError:
            return set()


def tokenize(s):
    clean_words = REGEX_TOKENIZER.tokenize(s)
    clean_words = [w.lower() for w in clean_words if w != '']
    return list(clean_words)


def lemmatize(tokens):
    lemmas = []
    for token in tokens:
        if re.match(r'[А-Яа-яёЁ]', token):
            lemma = PYMORPHY2_ANALYZER.parse(token)[0].normal_form
            lemmas.append(lemma)
        else:
            lemmas.append(token)
    return lemmas


def get_notation(operands):
    result = []
    stack = []
    for operand in operands:
        if operand not in OPERATORS:
            result.append(operand)
        else:
            last = None if len(stack) == 0 else stack[-1]
            while PRIORITY.get(last, -1) >= PRIORITY.get(operand, -1):
                result.append(stack.pop())
                last = None if not stack else stack[-1]
            stack.append(operand)
    for el in reversed(stack):
        result.append(el)
    return result


def evaluate(tokens):
    stack = []
    for token in tokens:
        if token in OPERATORS:
            arg2, arg1 = stack.pop(), stack.pop()
            if token == '&':
                result = arg1 & arg2
            else:
                result = arg1 | arg2
            stack.append(result)
        else:
            stack.append(get_index(token))
    return stack.pop()


def tokenize_query(query):
    negations_indices = []
    tokenized_query = []

    for (index, word) in enumerate(query.split(' ')):
        if word in OPERATORS:
            tokenized_query.append(word)
        else:
            if word[0] == '~':
                tokenized_word = lemmatize(tokenize(word[1:]))[0]
                tokenized_query.append('~' + tokenized_word)
            else:
                tokenized_word = lemmatize(tokenize(word))[0]
                tokenized_query.append(tokenized_word)

    return tokenized_query


if __name__ == '__main__':
    QUERY = sys.argv[1]
    tokenized_query = tokenize_query(QUERY)
    converted_query = get_notation(tokenized_query)
    result = evaluate(converted_query)
    print(result)
