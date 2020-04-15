from app import app, db
from models import User, Meditation
from flask import json, render_template, request
from markupsafe import escape
from telegram import telegram as tg


def get_user(json_obj):
    telegram_id = json_obj['message']['from'].get('id')
    user = User.query.filter(User.telegram_id == telegram_id).first()
    if user:
        pass #user is already registered
    else:
        user = register_new_user(json_obj)
    return user

def handle_message(user, client_answer):
    message_id_to_reply = client_answer['message'].get('message_id') #message id
    client_msg = client_answer['message'].get('text') #message text

    type_of_msg = lambda client_answer: 'reply' if client_answer['message'].get('reply_to_message') else 'ordinary_msg'
    type_of_msg = type_of_msg(client_answer)
    check = Meditation.check_if_not_finished_med_exists(user)

    if check['exist'] == True:
        show_finish_button = True
    else:
        show_finish_button = False

    if type_of_msg == 'ordinary_msg':
        if client_msg == '/start':
            tg.send_first_screen(user.telegram_id, show_finish_button=show_finish_button)
        elif client_msg == '🙌 Start meditation':
            check = Meditation.check_if_not_finished_med_exists(user)
            if check['exist'] == True:
                msg = 'You already a have not finished session. First, finish it.'
                tg.send_first_screen(user.telegram_id, msg, show_finish_button=True)
            else:
                new_meditation = Meditation(user)
                new_meditation.ask_for_duration(user, message_id_to_reply, 'new')
        elif client_msg == '⚡️ Add meditation':
            new_meditation = Meditation(user, was_added_after_session=1)
            new_meditation.ask_for_duration(user, message_id_to_reply, 'old')
        elif client_msg == '💡 Get stat':
            pass
        elif client_msg == '🖐 Finish meditation':
            not_finished_meditation = check['meditation_obj']
            if not_finished_meditation:
                not_finished_meditation.finish_meditation(user)
            else:
                msg = 'Nothing to finish'
                tg.send_first_screen(user.telegram_id, msg)
    elif type_of_msg == 'reply':
        print('we got reply')
        check = Meditation.check_if_not_finished_med_exists(user)
        if check['exist'] == True:
            try:
                reply = client_msg
                meditation = check['meditation_obj']
                if check['type'] == 0:
                    print(0)
                    meditation.start_meditation(user, int(reply))
                elif check['type'] == 1:
                    print(1)
                    meditation.record_meditation(user, duration__day_month=reply)
                    msg = 'Ok, your session was added'
                    tg.send_first_screen(user.telegram_id, msg)

            except Exception as e:
                    raise
        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bot/', methods=['GET', 'POST'])
def bot_handler():
    if request.method == 'POST':
        client_answer = request.get_json()
        tg.write_json(client_answer)
        if 'message' in client_answer:
            user = get_user(client_answer)
            handle_message(user, client_answer)

    return 'bot'






@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    # return 'User %s' % username
    return 'User %s' % escape(username)

