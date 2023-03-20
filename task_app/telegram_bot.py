from django.db.models.signals import post_save
from django.dispatch import receiver

from task_app.models import TaskList
from task_manager.settings import bot_token, bot_chatID
import requests


def telegram_bot(instance):
    if instance.status.title == "Processing":
        send_text = (
            "https://api.telegram.org/bot"
            + bot_token
            + "/sendMessage?chat_id="
            + bot_chatID
            + "&parse_mode=Markdown&text="
            + "Задача в работе"
            + "\n"
            + "Тема - "
            + instance.title
            + "\n"
            + "Автор - "
            + instance.author.username
            + "\n"
            + "Исполнитель - "
            + instance.performer.username
            + "\n"
            + "Статус - в работе"
            + "\n"
            + "Ссылка - http://127.0.0.1:8000/task/"
            + str(instance.pk)
        )
    elif instance.status.title == "Waiting":
        send_text = (
            "https://api.telegram.org/bot"
            + bot_token
            + "/sendMessage?chat_id="
            + bot_chatID
            + "&parse_mode=Markdown&text="
            + "Задача в ожидании назначения"
            + "\n"
            + "Тема - "
            + instance.title
            + "\n"
            + "Автор - "
            + instance.author.username
            + "\n"
            + "Исполнитель - "
            + "\n"
            + "Статус - в ожидании"
            + "\n"
            + "Ссылка - http://127.0.0.1:8000/task/"
            + str(instance.pk)
        )
    elif instance.status.title == "Solved":
        send_text = (
            "https://api.telegram.org/bot"
            + bot_token
            + "/sendMessage?chat_id="
            + bot_chatID
            + "&parse_mode=Markdown&text="
            + "Задача решена"
            + "\n"
            + "Тема - "
            + instance.title
            + "\n"
            + "Автор - "
            + instance.author.username
            + "\n"
            + "Исполнитель - "
            + instance.performer.username
            + "\n"
            + "Статус - Решена"
            + "\n"
            + "Ссылка - http://127.0.0.1:8000/task/"
            + str(instance.pk)
        )
    response = requests.get(send_text)
    return response.json()


@receiver(post_save, sender=TaskList, dispatch_uid="update_task")
def update_task(sender, instance, created, **kwargs):
    telegram_bot(instance)
