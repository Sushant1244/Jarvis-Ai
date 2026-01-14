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


def ai_stream(prompt_text, context=None):
    """Yield partial AI response chunks using OpenAI streaming API when available.
    Falls back to yielding the full answer once.
    """
    key = os.environ.get('OPENAI_API_KEY')
    if not key or openai is None:
        # fallback: single chunk
        ans = ai_answer(prompt_text, lang= None)
        if ans is None:
            yield ""
        else:
            yield ans
        return

    openai.api_key = key
    try:
        # Build simple conversation messages if context provided
        messages = []
        if context:
            for turn in context:
                role = turn.get('role', 'user')
                content = turn.get('content', '')
                messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": prompt_text})

        resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, stream=True)
        buffer = ''
        for chunk in resp:
            # chunk is a dict with choices->delta->content
            try:
                delta = chunk.choices[0].delta
                content = delta.get('content', '')
                if content:
                    buffer += content
                    # yield sooner for lower latency: at sentence end or every 30 chars
                    if content.endswith(('.', '!', '?')) or len(buffer) > 30:
                        yield buffer
                        buffer = ''
            except Exception:
                continue
        if buffer:
            yield buffer
    except Exception:
        # streaming failed; fallback to single answer
        ans = ai_answer(prompt_text)
        if ans:
            yield ans
        else:
            yield ""
