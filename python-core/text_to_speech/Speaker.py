import pyttsx3

class Speaker:

    def speak(self, audio):
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        voice_index = 2 # 1 is supposed to be a female voice
        
        engine.setProperty('voice', voices[voice_index].id)
        engine.say(audio)
        engine.runAndWait()