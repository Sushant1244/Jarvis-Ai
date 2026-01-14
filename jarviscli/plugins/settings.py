from ..plugin import plugin

@plugin('set name')
def set_name(jarvis, s):
    """Set assistant name: set name <name>
    """
    if not s:
        jarvis.say('Usage: set name <name>')
        return
    jarvis.update_data('assistant_name', s)
    jarvis.say(f'Okay, my name is now {s}')

@plugin('set voice')
def set_voice(jarvis, s):
    """Set voice: set voice <female|male>
    """
    if not s:
        jarvis.say('Usage: set voice <female|male>')
        return
    v = s.strip().lower()
    if v not in ('female', 'male'):
        jarvis.say('Voice must be female or male')
        return
    jarvis.update_data('voice_gender', v)
    jarvis.say(f'Voice set to {v}')

@plugin('set language')
def set_language(jarvis, s):
    """Set language for TTS: set language <en|hi|ne|mai|hi-en>
    """
    if not s:
        jarvis.say('Usage: set language <code>')
        return
    jarvis.update_data('voice_language', s.strip())
    jarvis.say(f'Language set to {s.strip()}')
