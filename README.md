# Интерфейс на PySide6 для взаимодействия с локальными LLM моделями Ollama

Представляет из себя диалоговое окно с возможностью написать текст и отправить его Ollama. После чего получить ответ.
* По умолчанию введена llama3.1

Данная версия тестовая и будет развиваться в менеджер чатов. Планируются возможности:
* Создавать отдельные динамические чаты с разными моделями и надстройками.
* Учет и анализ чатов, закрепление.

## Установка
```bash
git clone https://github.com/youshika-ypite/Ollama-chat-with-UI.git

python -m venv venv
venv\Scripts\activate

pip install Ollama, PySide6
```
## Запуск
```bash
venv\Scripts\activate
app.py
```

## Модель
Чтобы изменить модель. Необходимо в файле app.py поменять желаемую модель (ссылка `MODEL`)