import requests
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # Keep it in .env


def summarize_with_groq(content: str) -> str:
    if not GROQ_API_KEY:
        raise Exception("GROQ_API_KEY not found in environment")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes content."},
            {"role": "user", "content": f"Summarize the following content:\n\n{content}"}
        ],
        "model": "llama3-8b-8192",  # You can change this to mistral-7b if needed
        "temperature": 0.5,
        "max_tokens": 512,
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"GROQ API Error: {response.status_code} - {response.text}")

    result = response.json()
    return result['choices'][0]['message']['content'].strip()


def analyze_sentiment_with_groq(content: str) -> str:
    """
    Returns the sentiment of the content: Positive, Negative, or Neutral.
    """
    headers = {
    "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
    "Content-Type": "application/json",
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system",
             "content": "You are a sentiment analysis expert. Respond with only 'Positive', 'Negative', or 'Neutral'."},
            {"role": "user", "content": f"What is the sentiment of the following text?\n\n{content}"}
        ],
        "temperature": 0,
        "max_tokens": 10
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    result = response.json()
    return result['choices'][0]['message']['content'].strip()


def extract_topics_with_groq(content: str) -> list[str]:
    """
    Extracts main topics from the content and returns a list.
    """
    headers = {
    "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
    "Content-Type": "application/json",
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Extract key topics from the given content as a Python list of strings."},
            {"role": "user", "content": f"Extract topics:\n\n{content}"}
        ],
        "temperature": 0.2,
        "max_tokens": 100
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    output = response.json()['choices'][0]['message']['content'].strip()

    try:
        topics = eval(output)
        if isinstance(topics, list):
            return topics
    except:
        return [output]

    return [output]


def recommend_related_with_groq(content: str, articles: list[str]) -> list[str]:
    """
    Given the content and a list of article titles/snippets, return which are most related.
    """
    content_snippets = "\n".join([f"{i+1}. {a}" for i, a in enumerate(articles)])
    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are an AI assistant that finds related content."},
            {
                "role": "user",
                "content": f"""Given this content:"{content} And these articles/snippets:
                {content_snippets} Return the numbers of the top 2 most related articles.""",
            }
        ],
        "temperature": 0.3,
        "max_tokens": 50
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    return response.json()['choices'][0]['message']['content'].strip()
