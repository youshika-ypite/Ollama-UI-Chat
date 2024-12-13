import os
import json

class PageData:
    """
    Класс для хранения и обработки данных чата.
    """

    def __init__(self,
        name: str = "StdPageName",
        chat_history:  list[dict] = []
        ):
        
        self.name = name
        self.chat_history = chat_history

    def get_data(self) -> dict[str, any]:
        """
        Возвращает все данные для сохранения в json формате

        История чата не отфильтрованна, учитывает сообщения всех ролей.
        ```
        {
            "name": str,
            "chat_history": list[dict[str, any]]
        }
        ```
        """
        data = {
            "name": self.name,
            "chat_history": self.chat_history
        }
        return data

    def get_chat_history(self) -> list[dict[str, str]]:

        lc = self.chat_history.copy()

        return lc

    def set_name(self, name: str): self.name = name
    def set_chat_history(self, history: list[dict[str, any]]):
        self.chat_history = history

    def set_data(self, data: dict[str, any]):
        """Принимает данные для восстановления страницы

        Формат такой же, как при методе `set_data`
        ```
        {
            "name": str,
            "chat_history": list[dict[str, any]]
        }
        ```
        """
        self.name = data["name"]
        self.chat_history = data["chat_history"]


class Config:

    config = json.load(open("data/config.json", "r", encoding="utf-8"))
    bd = {"chats": {}}
    if not os.path.exists("data/chats.json"):
        file = open("data/chats.json", "w+", encoding="utf-8")
        json.dump(bd, file, indent=4, ensure_ascii=False)
        file.close()
    
    chats = json.load(open("data/chats.json", "r", encoding="utf-8"))

    THEMES = ["message_light.css", "message_dark.css"]
    theme = config["settings"]["theme"] 

    @staticmethod
    def _get_config() -> dict:
        return Config.config
    
    @staticmethod
    def _get_chats() -> dict:
        return Config.chats

    @staticmethod
    def get_settings() -> dict:
        copyied = Config._get_config().copy()
        return copyied["settings"]
    
    @staticmethod
    def get_user_name() -> str:
        return Config.get_settings()["user_name"]

    @staticmethod
    def get_theme() -> str:
        return Config.get_settings()["theme"]

    @staticmethod
    def get_ollama_name() -> str:
        return Config.get_settings()["ollama_model"]
    
    @staticmethod
    def get_chats() -> dict:
        copyied = Config._get_chats().copy()
        return copyied["chats"]
    
    @staticmethod
    def get_chat_wname(name: str) -> bool|dict[str, any]:
        copyied = Config._get_chats().copy()
        if name in copyied["chats"]:
            return copyied["chats"]["name"]
        else:
            return False
        
    @staticmethod
    def update_chat(data: dict):
        Config.chats["chats"][data["name"]] = data

    @staticmethod
    def delete_chat(name: str):
        if name in Config.chats["chats"]:
            Config.chats["chats"].pop(name)

    @staticmethod
    def search(name: str) -> dict|None:
        """Ищет чат по его имени, если чат найден - возвращает его данные,
        иначе - `None`"""
        if name in Config.chats["chats"]:
            return Config.chats["chats"][name].copy()
        else: return None

    @staticmethod
    def get_theme() -> str:
        return Config.THEMES[Config.theme]
    
    @staticmethod
    def get_theme_index() -> int:
        return Config.theme

    @staticmethod
    def change_theme(newindex: int):
        Config.theme = newindex
        Config.config["settings"]["theme"] = newindex
        return Config.get_theme()
    
    @staticmethod
    def get_user_icon() -> str:
        if Config.theme:
            return Config.config["icons"][2]
        else:
            return Config.config["icons"][0]
        
    @staticmethod
    def get_bot_icon() -> str:
        if Config.theme:
            return Config.config["icons"][3]
        else:
            return Config.config["icons"][1]

    @staticmethod
    def save():
        json.dump(
            obj=Config.config,
            fp=open("data/config.json", "w", encoding="utf-8"),
            indent=4,
            ensure_ascii=False
        )
        json.dump(
            obj=Config.chats,
            fp=open("data/chats.json", "w", encoding="utf-8"),
            indent=4,
            ensure_ascii=False
        )
