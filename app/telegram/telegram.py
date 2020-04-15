import json
# from models import User, Meditation
from config import URL
import requests

def write_json(data, filename='answer_client.json'):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, indent = 4, ensure_ascii=False)

def register_new_user(json_obj):
    telegram_id = json_obj['message']['from'].get('id')
    username = json_obj['message']['from'].get('username')
    first_name = json_obj['message']['from'].get('first_name')
    second_name = json_obj['message']['from'].get('last_name')
    new_user = User(telegram_id, username, first_name, second_name)
    return new_user

def send_message(chat_id, text, reply_keyboard_markup='', disable_web_page_preview=False):
    url = URL + 'sendMessage'
    if reply_keyboard_markup == '':
        answer = {'parse_mode': 'html', 'chat_id': chat_id, 'text': text, \
                 'disable_web_page_preview':disable_web_page_preview}
    else:
        answer = {'parse_mode': 'html', 'chat_id': chat_id, 'text': text, \
                 'reply_markup': reply_keyboard_markup, 'disable_web_page_preview':disable_web_page_preview}

    r = requests.post(url, json=answer)
    return r.json()

def reply_to_message(chat_id, message_id, text):
    url = URL + 'sendMessage'
    answer = {'parse_mode': 'html', 'chat_id': chat_id, 'text': text, 'reply_to_message_id': message_id, \
             'reply_markup':{'force_reply':True}}
    r = requests.post(url, json=answer)
    return r.json()

def send_first_screen(chat_id, msg='Main', show_finish_button=False):
    if show_finish_button == True:
        reply_keyboard_markup_keyboard = [['🖐 Finish meditation']]
    else:
        reply_keyboard_markup_keyboard = [['🙌 Start meditation'], ['⚡️ Add meditation']] #, ['⚡️ Add meditation'], ['💡 Get stat']

    reply_keyboard_markup = {
            'keyboard': reply_keyboard_markup_keyboard, 'resize_keyboard': True,
            'one_time_keyboard': False
        }

    reply_keyboard_markup = json.dumps(reply_keyboard_markup)  # конвертируем в json-формат
    send_message(chat_id, msg, reply_keyboard_markup)




# def send_photo(chat_id, photo_url, caption, reply_markup=''):
#     url = URL + 'sendPhoto'
#     photo_url = ''
#     if reply_markup == '':
#         answer = {'parse_mode': 'html', 'chat_id': chat_id, 'photo': photo_url, 'caption': caption}
#     else:
#         answer = {'parse_mode': 'html', 'chat_id': chat_id, 'photo': photo_url, 'caption': caption,
#                   'reply_markup': reply_markup}
#     r = requests.post(url, json=answer)
#     print(answer)
#     print('sendPhoto', r.text)
#     return r.json()





