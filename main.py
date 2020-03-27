from models import User, Meditation


user_1 = User('Dmitry','Smirnov')
print(user_1)

med_1 = Meditation()
med_1.start_meditation(1)
print(med_1)

user_1.add_meditation(med_1)

print(user_1.meditations)
