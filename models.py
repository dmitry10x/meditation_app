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

    def finish_meditation(self, duration_minutes):
        self.time_end = self.time_start + datetime.timedelta(minutes=duration_minutes)
        print('Помедитировали..')

    def start_meditation(self, duration_minutes):
        print('Начинаем медитировать {} минут..'.format(duration_minutes))
        self.time_start = datetime.datetime.now()
        time.sleep(duration_minutes*60)
        Meditation.finish_meditation(self, duration_minutes)

    def __repr__(self):
        return '--> Meditation {}'.format(self.id, self.time_start, self.time_end)


def main():
    print('Hello! You`ve launched models.py')


if __name__ == '__main__':
    main()
else:
    pass
