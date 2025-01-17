# save the time into a file a
import datetime
time = datetime.datetime.now()
with open('time.txt', 'w') as f:
    f.write(str(time))
