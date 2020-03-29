import datetime
import time


class User:
    num_of_users = 0
    def __init__(self, first_name, second_name, meditations=None):
        self.first_name = first_name
        self.second_name = second_name

        if meditations is None:
            self.meditations = []
        else:
            self.meditations = meditations

        User.num_of_users += 1

    def add_meditation(self, meditation):
        if meditation not in self.meditations:
            self.meditations.append(meditation)

    def remove_meditation(self, meditation):
        if meditation in self.meditations:
            self.meditations.remove(meditation)

    def __repr__(self):
        return 'User {} {}'.format(self.first_name, self.second_name)


class Meditation:
    num_of_meditations = 0
    def __init__(self):
        self.id = Meditation.num_of_meditations + 1
        self.time_start = None
        self.time_end = None

        Meditation.num_of_meditations += 1

    def describe_session(self):
        duration = (self.time_end - self.time_start).total_seconds() // 60
        print('Meditation №{}\nDuration: {} min.'.format(self.id, int(duration)))

    def finish_meditation(self):
        msg = input("Time is up..\nEnter 'OK' when you are ready to finish your session: ")
        if msg.lower() == 'ok':
            self.time_end = datetime.datetime.now()
        else:
            Meditation.finish_meditation(self)

    def ask_for_duration(self):
        duration_minutes = input('How long are you going to meditate? (min): ')
        return duration_minutes

    def start_meditation(self):
        duration_minutes = self.ask_for_duration()
        print('Meditation for {} min. has started..'.format(duration_minutes))
        self.time_start = datetime.datetime.now()
        time.sleep(int(duration_minutes)*60)
        Meditation.finish_meditation(self)

    def record_meditation(self, day_month_year, duration):
        """
        day_month_year has to be in format: 29.3.20 - 29th of March, 2020;
        duration in minutes
        """
        day, month, year = day_month_year.split('.')
        self.time_start = datetime.datetime(int(year), int(month), int(day))
        self.time_end = self.time_start + datetime.timedelta(minutes=duration)
        return self

    def __repr__(self):
        return '--> Meditation {}'.format(self.id, self.time_start, self.time_end)


def main():
    print('Hello! You`ve launched models.py')


if __name__ == '__main__':
    main()
else:
    pass
