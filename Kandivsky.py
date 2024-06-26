import requests
import json
from bs4 import BeautifulSoup
import uuid

auth = ''

def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    # Создадим идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {
        'scope': scope
    }

    try:
        # Делаем POST запрос с отключенной SSL верификацией
        # (можно скачать сертификаты Минцифры, тогда отключать проверку не надо)
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1
response = get_token(auth)

if response != 1:
  print(response.text)
  giga_token = response.json()['access_token']

def send_chat_request(giga_token, user_message):

    # URL API для отправки запросов к GigaChat
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Заголовки для HTTP-запроса
    headers = {
        'Content-Type': 'application/json',  # Указываем, что отправляемые данные в формате JSON
        'Authorization': f'Bearer {giga_token}',  # Используем токен авторизации для доступа к API
    }

    # Данные для отправки в теле запроса
    payload = {
        "model": "GigaChat:latest",  # Указываем, что хотим использовать последнюю версию модели GigaChat
        "messages": [
            {
                "role": "user",  # Роль отправителя - пользователь
                "content": user_message  # Сообщение от пользователя
            },
        ],
        "temperature": 0.7  # Устанавливаем температуру, чтобы управлять случайностью ответов
    }

    try:
        # Отправляем POST-запрос к API и получаем ответ
        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
        # Выводим текст ответа. В реальных условиях следует обрабатывать ответ и проверять статус коды.
        print(response.json())
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        # В случае возникновения исключения в процессе выполнения запроса, выводим ошибку
        print(f"Произошла ошибка: {str(e)}")
        return None

def prints(message):
    response_img_tag = send_chat_request(giga_token, message)
    print(response_img_tag)

    # Парсим HTML
    soup = BeautifulSoup(response_img_tag, 'html.parser')

    # Извлекаем значение атрибута `src`
    img_src = soup.img['src']

    print(img_src)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {giga_token}',
    }

    response = requests.get(f'https://gigachat.devices.sberbank.ru/api/v1/files/{img_src}/content', headers=headers,
                            verify=False)

    with open('image.jpg', 'wb') as f:
        f.write(response.content)
    return "image.jpg"
