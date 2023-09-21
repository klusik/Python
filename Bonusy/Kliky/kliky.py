import winsound
import time

from time import gmtime, strftime


kliky = 30
while True:
    time.sleep(15*60)

    winsound.Beep(37, 2000)

    winsound.Beep(392, 500)
    winsound.Beep(392, 500)
    winsound.Beep(392, 500)

    winsound.Beep(311, 1000)

    time.sleep(1)

    winsound.Beep(349, 500)
    winsound.Beep(349, 500)
    winsound.Beep(349, 500)

    winsound.Beep(293, 1000)

    kliky += 15

    print(strftime("%H:%M:%S", gmtime()))
    print(kliky)
    print()
    time.sleep(2)

