import math
import numpy as np

from collections import defaultdict, Counter

def compute_idfs(tokens_per_document):
    token_counts = defaultdict(int)
    document_term_count = defaultdict(int)
    document_count = len(tokens_per_document)

    for document in tokens_per_document:
        term_counts = Counter(document)
        for token, count in term_counts.iteritems():
            document_term_count[token] += 1
            token_counts[token] += count

    # Remove rare words
    to_remove = []
    for token, count in token_counts.iteritems():
        if count < 5:
            to_remove.append(token)

    for token in to_remove:
        del document_term_count[token]
        del token_counts[token]

    def idf(token):
        idf = math.log(1. + float(document_count) / document_term_count[token])
        return idf

    return {token: idf(t) for token in token_counts}

def compute_names_vector(data, vsm_idfs):
    names = []
    vsm = np.zeros((len(data), len(vsm_idfs)))
    for i, document in enumerate(data):
        document_terms = Counter(document["tokens"])
        total_terms = len(document["tokens"])
        name = document["name"]
        names.append(name)
        for j, term in enumerate(vsm_idfs.keys()):
            vsm[i, j] = float(document_terms[term]) / total_terms * vsm_idfs[term]
    return names, vsm
