import os
from groq import Groq


# ── Put your Groq API key here ──────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

client = Groq(api_key=GROQ_API_KEY)

# Model to use — fast & capable; swap to "llama3-70b-8192" for heavier tasks
MODEL = "llama-3.1-8b-instant"


def _chat(prompt: str) -> str:
    """Internal helper: send a single-turn prompt and return the reply text."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def generate_roadmap(topic: str) -> str:
    prompt = f"""
    Create a clear, structured learning roadmap for: "{topic}".

    Format it as numbered stages with bold titles. Be practical and progressive.
    Cover beginner to advanced. Keep it under 300 words.
    Use markdown formatting.
    """
    try:
        return _chat(prompt)
    except Exception as e:
        return f"Error generating roadmap: {str(e)}"


def generate_explanation(topic: str) -> str:
    prompt = f"""
    Give a clear, engaging explanation of "{topic}" for a motivated learner.

    Cover:
    - What it is
    - Why it matters
    - Key concepts and real-world use cases

    Use simple language. Keep it under 250 words. Use markdown formatting.
    """
    try:
        return _chat(prompt)
    except Exception as e:
        return f"Error generating explanation: {str(e)}"


def generate_resources(topic: str) -> str:
    prompt = f"""
    List 5-6 top learning resources for "{topic}".

    Include a mix of:
    - Free online courses (Coursera, edX, YouTube)
    - Books (beginner and advanced)
    - Websites and documentation
    - Paid courses if highly recommended

    Format as a clean markdown list with brief descriptions for each.
    Keep it under 200 words.
    """
    try:
        return _chat(prompt)
    except Exception as e:
        return f"Error generating resources: {str(e)}"


def chatbot_response(question: str) -> str:
    prompt = f"""
    You are Learnova, an expert AI learning mentor. A student asks:

    "{question}"

    Give a helpful, concise, and encouraging response. Max 150 words.
    Use markdown formatting where helpful.
    """
    try:
        return _chat(prompt)
    except Exception as e:
        return f"Sorry, I couldn't respond right now. Error: {str(e)}"
