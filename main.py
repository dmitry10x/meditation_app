from models import User, Meditation


user_1 = User('Dmitry','Smirnov')
print(user_1)


# med_1 = Meditation()
# med_1.start_meditation()
# med_1.describe_session()


# med_2 = Meditation()
# med_2.start_meditation()
# med_2.describe_session()


# user_1.add_meditation(med_1)

# print(user_1.meditations)

med_old = Meditation()
med_old.record_meditation('29.03.20',6)

print(med_old.describe_session())
