import queue
import threading
from time import sleep
from gpt4all import GPT4All
from communication.WebSocketsClient import WebSocketsClient

from text_to_speech.Speaker import Speaker

class Gpt4AllBrain:

    def speaker_worker(self):
        while True:
            item = self.speaker_queue.get()
            self.speaker.speak(item)
            self.speaker_queue.task_done

    def writer_worker(self):
        while True:
            w_token = self.writer_queue.get()
            sleep(0.17)
            print(w_token, end="", flush=True)
            self.websockets_client.send(self.get_message_obj(w_token))
            self.writer_queue.task_done

    def get_message_obj(self, token):
        message_obj = {
            "source": "brain",
            "target": "client",
            "content": token
        }

        return message_obj

    def __init__(self) -> None:
        self.websockets_client = WebSocketsClient()
        self.speaker_queue = queue.Queue()
        self.writer_queue = queue.Queue()
        self.speaker = Speaker()

        # Models are automatically downloaded in C:\Users\(current_user)\.cache\gpt4all
        # Other models to use:
        # -> llama-2-7b-chat.ggmlv3.q4_0.bin
        # -> GPT4All-13B-snoozy.ggmlv3.q4_0.bin
        # -> orca-mini-3b.ggmlv3.q4_0.bin
        self.model = GPT4All("orca-mini-3b.ggmlv3.q4_0.bin")        

        threading.Thread(target=self.speaker_worker, daemon=True).start()
        threading.Thread(target=self.writer_worker, daemon=True).start()

    def get_end_char_index(self, token_phrase):
        end_phrase_char_index = []
        end_chars = [" ", ",", ".", ":", ";", "\r"]

        for end_char in end_chars:
            end_phrase_char_index.append(token_phrase.rfind(end_char))

        return min(char_index for char_index in end_phrase_char_index if char_index > 0)

    def run_query(self, query):

        token_phrase = ""

        for token in self.model.generate(query, max_tokens=500, streaming=True):
            self.writer_queue.put(token)
            token_phrase += token
                
            if len(token_phrase) > 150:
                last_separator_index = self.get_end_char_index(token_phrase)
                phrase_to_add = token_phrase[0: last_separator_index]
                last_word_segment = token_phrase[last_separator_index: len(token_phrase)]

                token_phrase = last_word_segment
                self.speaker_queue.put(phrase_to_add)

        if len(token_phrase) > 0:
            self.speaker_queue.put(token_phrase)
