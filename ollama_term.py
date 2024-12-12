import ollama

from config import Config

from typing import AnyStr
from typing import Mapping, Iterator
from typing import Optional, Sequence

ROLE = "role"
CONTENT = "content"

USER = "user"
SYSTEM = "system"
ASSISTANT = "assistant"

config = Config()

OLLAMA_PARAMS = {
    "options": {
        "io_timeout": 10,
    },
    "options_other": {
        #"mirostat": 0,
        #"mirostat_eta": 0.1,
        #"mirostat_tau": 5.0,
        #"num_ctx": 2048,
        #"num_gqa": 4,
        #"num_gpu": 1,
        #"num_thread": 64,
        #"repeat_last_n": 1.1,
        #"temperature": 0.8,
        #"seed": 0,
        #"stop": "stop",
        #"tfs_z": 1,
        #"num_predict": 128,
        #"top_k": 40,
        #"top_p": 0.9
    }
}

class Ollama:
    """Create an Ollama client"""
    client = ollama.Client()
    active_chat_history = []

    def set_chat_history(self, chat_history: list[dict[str, any]]):
        self.active_chat_history = chat_history

    def get_chat_history(self) -> list[dict[str, any]]:
        return self.active_chat_history.copy()

    def send_message(self, text: str) -> Iterator[Mapping[str, any]]:
        self.active_chat_history.append({ROLE: USER, CONTENT: text})
        response = self.client.chat(
            model=config.get_ollama_name(),
            messages=self.active_chat_history,
            options=OLLAMA_PARAMS["options"],
            stream=True
            )
        self.set_message_role()
        return response

    def set_message_role(self, index: int = -1, ROLETAG: str = SYSTEM):
        self.active_chat_history[index][ROLE] = ROLETAG
    
    # Сохранение ответа самой модели
    def append_response(self, response: str) -> None:
        self.active_chat_history.append({ROLE: ASSISTANT, CONTENT: response})

    # Заготовка для обработки сообщения вне контекста сообщений или обработки изобажения
    def generate_response(self,
        prompt: str = '',
        images: Optional[Sequence[AnyStr]] = None
        ) -> bool|Iterator[Mapping[str, any]]:
        
        """Форма получения ответа: `response['response']`"""
        if images is None and prompt == '': return 0
        response = self.client.generate(
            model=config.get_ollama_name(),
            options=OLLAMA_PARAMS["options"],
            prompt=prompt,
            images=images,
            stream=True
            )
        return response

    # Delete request, history.. and other getters & setters