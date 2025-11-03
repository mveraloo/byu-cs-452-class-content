import pandas as pd
import numpy as np
import json
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity


with open("config.json") as configFile:
    config = json.load(configFile)["openaiKey"]
client = OpenAI(api_key=config)

questions = [
    "How can I gain a testimony of Jesus Christ?",
    "What are some ways to deal with challenges in life and find a purpose?",
    "How can I fix my car if it won't start?"
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

def get_openai_embeddings(questions):
    
    response = client.embeddings.create(input=questions, model="text-embedding-3-small")
    embeddings = [np.array(data_point.embedding) for data_point in response.data]
    return embeddings

def clean_text(text):
    if isinstance(text, str):
        if text.startswith("['") and text.endswith("']"):
            return text[2:-2]
        return text
    elif isinstance(text, list):
        return ' '.join(text)
    return str(text)

def getChatGptResponse(content):
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)
    print()
    result = "".join(responseList)
    return result

def generate_chatgpt_response_with_talks(question, top_talks):
    context = "Here are some relevant conference talks:\n\n"
    for n, (_, row) in enumerate(top_talks.iterrows(), 1):
        context += f"{n}. Title: {row.title} by {row.speaker} ({row.calling})\n"
        context += f"   Excerpt: {clean_text(row.text)[:200]}...\n\n"

    prompt = f"{context}\nUsing the above talks as context, answer the following question:\n{question}\n"
    return getChatGptResponse(prompt)

def conference_rag():
    print("=" * 80)
    print("RAG SYSTEM: ChatGPT Generation with Talks Retrieval")
    print("")
    print("RETRIEVAL METHOD: Talks")
    print("=" * 80)

    openai_talks = pd.read_csv("openai/openai_talks.csv")
    question_embeddings = get_openai_embeddings(questions)
    print("")
    print("RAG System")
    print("")

    for index, question in enumerate(questions):
        print(f"\n# Question {index+1}: {question}")
        question_embedding = question_embeddings[index]
    
        top_talks = find_similar_talks(question_embedding, openai_talks, top_k=3)

        print("Top 3 Similar Talks:")
        print("")
        for n, (_, row) in enumerate(top_talks.iterrows(), 1):
            print(f"{n}. {row.title} by {row.speaker}")
            print(f"   Similarity: {row.similarity:.4f}")
            print(f"   Talk: {clean_text(row.text)[:150]}...")
            print()

        # Generate ChatGPT response
        print("ChatGPT Response:")
        print("-" * 50)
        chatgpt_response = generate_chatgpt_response_with_talks(question, top_talks)
        print(chatgpt_response)
        print("=" * 80)

if __name__ == "__main__":
    conference_rag()