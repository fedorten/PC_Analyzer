import ssl
import gigachat
from pc_analizer import get_pc_info

# Создаем SSL контекст без проверки
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Инициализируем GigaChat
giga = gigachat.GigaChat(
    credentials="MDE5YzE5MWYtYWVmMy03MjUyLTg0MjgtMDcyODYzNjBkYzVkOmZkOThmNmUxLTk0MjAtNGViNS1iZDRhLTJiNzAyNzM5YmZkNQ==",
    ssl_context=ssl_context,
    verify_ssl_certs=False,
)


def ai_response(prompt):
    try:
        response = giga.chat(
            str(get_pc_info()) + "обьясни состояние пк простым языком" + prompt
        )
        print("\nОтвет GigaChat:", response.choices[0].message.content)
        response_text = response.choices[0].message.content
        return response_text

    except Exception as e:
        print(f"Ошибка: {e}")


ai_response("привет")
