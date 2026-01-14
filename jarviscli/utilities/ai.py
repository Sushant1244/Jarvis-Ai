import os
try:
    import openai
except Exception:
    openai = None


def ai_answer(prompt_text, lang=None):
    """Return AI-generated answer for prompt_text using OpenAI if available.
    Returns None if no key or openai not installed.
    """
    key = os.environ.get('OPENAI_API_KEY')
    if not key or openai is None:
        return None

    openai.api_key = key
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt_text}],
            max_tokens=200,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None
