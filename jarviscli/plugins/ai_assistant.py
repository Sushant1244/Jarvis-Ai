from plugin import plugin
from jarviscli.utilities import ai as ai_util


@plugin('ask')
def ask(jarvis, s):
    """Ask the AI assistant a single question.

    Usage: ask <question>
    """
    question = s.strip()
    if not question:
        jarvis.say('Please provide a question.')
        return

    jarvis.say('Thinking...')
    answer = ai_util.ai_answer(question)
    if answer:
        jarvis.say(answer)
    else:
        jarvis.say("AI is not configured or not available. Please set OPENAI_API_KEY or try again later.")


@plugin('chat')
def chat(jarvis, s):
    """Start an interactive chat with the AI.

    Type 'exit' or 'quit' to end the chat.
    """
    jarvis.say('Starting chat mode. Say "exit" to quit.')
    while True:
        try:
            jarvis.say('You:')
            user_input = jarvis.input()  # reuse jarvis's input hook
        except Exception:
            break
        text = (user_input or '').strip()
        if not text:
            continue
        if text.lower() in ('exit', 'quit'):
            jarvis.say('Exiting chat mode.')
            break

        jarvis.say('Thinking...')
        answer = ai_util.ai_answer(text)
        if answer:
            jarvis.say(answer)
        else:
            jarvis.say("AI not configured. Set OPENAI_API_KEY to enable AI responses.")
