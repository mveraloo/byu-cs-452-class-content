import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

questions = [
    "How can I gain a testimony of Jesus Christ?",
    "What are some ways to deal with challenges in life and find a purpose?",
    "How can I fix my car if it won't start?",
    "Can you recommend some talks about leadership?",
    "How can I strengthen my relationship with my boyfriend?"
]

def parse_embeddings(embedding_str):
    return np.array(eval(embedding_str))

def find_similar_talks(question_embedding, content, top_k=3):
    embeddings = content['embedding'].apply(parse_embeddings).tolist()
    embeddings_array = np.array(embeddings)

    similarities = cosine_similarity([question_embedding], embeddings_array)[0]
    content_2 = content.copy()
    content_2['similarity'] = similarities

    return content_2.nlargest(top_k, 'similarity')

def compare_content(talks, paragraphs, clusters, embedding_type = "free"):
    question_embeddings = model.encode(questions)
    results = {}

    print("Free Embeddings")
    print("")

    for index, question in enumerate(questions):
        print(f"\n# Question {index+1}: {question}")
        question_embedding = question_embeddings[index]
        
        similar_talks = find_similar_talks(question_embedding, talks, top_k=3)
        similar_paragraphs = find_similar_talks(question_embedding, paragraphs, top_k=3)
        similar_clusters = find_similar_talks(question_embedding, clusters, top_k=3)

        results[question] = {
            "talks": similar_talks,
            "paragraphs": similar_paragraphs,
            "clusters": similar_clusters
        }

        print("")
        print("Top 3 Similar Talks:")
        print("")
        for n, (_, row) in enumerate(similar_talks.iterrows(), 1):
            print(f"{n}. {row.title} {row.speaker} ({row.calling}):")
            print(f"    {row.text[:200]}...")

        
        print("")
        print("Top 3 Similar Paragraphs:")
        print("")
        for n, (_, row) in enumerate(similar_paragraphs.iterrows(), 1):
            print(f"{n}. {row.title} {row.speaker} ({row.calling}):")
            print(f"    {row.text[:200]}...")

        
        print("")
        print("Top 3 Similar Clusters:")
        print("")
        for n, (_, row) in enumerate(similar_clusters.iterrows(), 1):
            print(f"{n}.{row.title}{row.speaker} ({row.calling}):")
            print(f"    {row.text[:200]}...")
        print("=" *60)
        print("")



def main():
    free_talks = pd.read_csv("free/free_talks.csv")
    free_paragraphs = pd.read_csv("free/free_paragraphs.csv")
    free_clusters = pd.read_csv("free/free_3_clusters.csv")

    print("Comparing Free Embeddings Content")
    compare_content(free_talks, free_paragraphs, free_clusters, embedding_type="free")

if __name__ == "__main__":
    main()