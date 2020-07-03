from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx


def read_article(file_name):
    """
    This method reads the file and then does some preprocessing
    to generate clean text
    :param file_name:
    :return: List of sentences
    """

    filedata = file_name
    article = filedata.split(". ")
    sentences = []

    for sentence in article:
        sentences.append(sentence.replace("[a-zA-Z", " ").split(" "))
    sentences.pop()
    return sentences


def sentence_similarity(sentence1, sentence2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sentence1 = [word.lower() for word in sentence1]
    sentence2 = [word.lower() for word in sentence2]

    all_words = list(set(sentence1 + sentence2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    # building vector for the first sentence
    for word in sentence1:
        if word in stopwords:
            continue
        vector1[all_words.index(word)] += 1

    # building vector for the second sentence
    for word in sentence2:
        if word in stopwords:
            continue
        vector2[all_words.index(word)] += 1

    return 1 - cosine_distance(vector1, vector2)


def similarity_matrix(sentences, stop_words):
    sim_matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i == j:
                continue
            sim_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stop_words)
    return sim_matrix


def generate_summary(file_name, top_n=5) -> str:
    stop_words = stopwords.words('english')
    summarize_text = []

    sentences = read_article(file_name)
    sentences_sim_matrix = similarity_matrix(sentences, stop_words)
    sentences_sim_graph = nx.from_numpy_array(sentences_sim_matrix)
    scores = nx.pagerank(sentences_sim_graph)

    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))

    summarized_text = ". ".join(summarize_text)

    return summarized_text

