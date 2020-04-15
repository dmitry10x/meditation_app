from app import db
from telegram import telegram as tg
import datetime
import time
from sqlalchemy import and_


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(100))
    username = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    second_name = db.Column(db.String(20))
    registered = db.Column(db.DateTime)

    meditations = db.relationship('Meditation', backref='user', lazy=True)

    def __init__(self, telegram_id, username=None, first_name=None, second_name=None):
        self.telegram_id = telegram_id
        self.username = username
        self.first_name = first_name
        self.second_name = second_name
        self.registered = datetime.datetime.now()

        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete(cls, obj):
        db.session.delete(obj)
        db.session.commit()
        print('{} was deleted at {}'.format(obj, datetime.datetime.now()))


    # def add_meditation(self, meditation):
    #     if meditation not in self.meditations:
    #         self.meditations.append(meditation)

    # def remove_meditation(self, meditation):
    #     if meditation in self.meditations:
    #         self.meditations.remove(meditation)

    def __repr__(self):
        return 'User {} {} {}'.format(self.id, self.first_name, self.second_name)


class Meditation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_start = db.Column(db.DateTime)
    time_end = db.Column(db.DateTime)
    was_added_after_session = db.Column(db.Integer)

    def __init__(self, user, time_start=None, time_end=None, was_added_after_session=0):
        self.user_id = user.id
        self.time_start = time_start
        self.time_end = time_end
        self.was_added_after_session = was_added_after_session
        db.session.add(self)
        db.session.commit()


    # def describe_session(self):
    #     duration = (self.time_end - self.time_start).total_seconds() // 60
    #     print('Meditation №{}\nDuration: {} min.'.format(self.id, int(duration)))

    def finish_meditation(self, user):
        self.time_end = datetime.datetime.now()
        db.session.commit()
        duration_minutes = (self.time_end - self.time_start).total_seconds() // 60
        msg = 'Meditation is finished. — {} min\nGood for you.'.format(duration_minutes)
        tg.send_first_screen(user.telegram_id, msg)
        # if msg.lower() == 'ok':
        #     self.time_end = datetime.datetime.now()
        # else:
        #     Meditation.finish_meditation(self)

    def ask_for_duration(self, user, message_id_to_reply, meditation_type):
        if meditation_type == 'new':
            msg = 'How long are you going to meditate? (min): '
        elif meditation_type == 'old':
            msg = 'Type duration (min) and date like that:\n20min on the 15th of March 👉 <b>20-15.4</b>'
        tg.reply_to_message(user.telegram_id, message_id_to_reply, msg)

    def start_meditation(self, user, duration_minutes):
        msg = 'Meditation for {} min. has started..'.format(duration_minutes)
        tg.send_message(user.telegram_id, msg)
        self.time_start = datetime.datetime.now()
        db.session.commit()
        time.sleep(int(duration_minutes)*60)
        msg = 'Time is up..\nPress <b>Finish meditation</b> button when you are ready to finish your session'
        tg.send_first_screen(user.telegram_id, msg, show_finish_button=True)
        # Meditation.finish_meditation(self)

    @classmethod
    def check_if_not_finished_med_exists(cls, user):
        not_finished_meditation = Meditation.query.filter(and_(Meditation.user_id == User.id, \
                                  Meditation.time_end == None)).first()
        if not_finished_meditation:
            return {'exist': True, 'meditation_obj': not_finished_meditation, \
                    'type': not_finished_meditation.was_added_after_session}
        else:
            return {'exist': False, 'meditation_obj': None}

    def record_meditation(self, user, duration__day_month):
        """
        duration__day_month has to be in format: 8-29.3 - 9 minutes on the 29th of March;
        duration in minutes
        """
        print('record_meditation')
        duration, day_month = duration__day_month.split('-')
        day, month = day_month.split('.')
        this_year = datetime.datetime.today().year
        self.time_start = datetime.datetime(int(this_year), int(month), int(day))
        self.time_end = self.time_start + datetime.timedelta(minutes=int(duration))
        print(self)
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '--> Meditation {}'.format(self.id, self.time_start, self.time_end)


def main():
    print('Hello! You`ve launched models.py')


if __name__ == '__main__':
    main()
else:
    pass
