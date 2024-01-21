from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_neurals(user_query: str, descriptions: list[str], output_num: int) -> list[str]:
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(descriptions + [user_query])

    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    tfidf_matches = sorted(enumerate(cosine_similarities), key=lambda x: x[1], reverse=True)

    # for match in tfidf_matches[:3]:
    #     print(f"Описание: {descriptions[match[0]]}, Сходство: {match[1]:.4f}")

    return list(map(lambda x: x[0], tfidf_matches[:output_num]))
