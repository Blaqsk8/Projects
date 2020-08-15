#!python
# File happynumbers.py

"""
Starting with any positive integer, replace the number by the sum of the squares of its digits, and repeat the process
until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
Those numbers for which this process ends in 1 are happy numbers, while those that do not end in 1 are unhappy numbers.
"""

import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget


def digitssquared(arg1):
    number = arg1
    newnum = 0
    for i in number:
        numsqr = (int(i) ** 2)
        print(i, 'squared is', numsqr)
        print("%d + %d = %d" % (newnum, numsqr, (newnum + numsqr)))
        newnum = newnum + numsqr
        # print(i, 'squared is', numsqr)
    # happy_field.insert(10, newnum)
    return newnum

def digitscubed(arg1):
    numcubed = int(arg1) ** 3
    print("%s cubed is %d" % (arg1, numcubed))
    return numcubed


def happy():
    digitscubed(int(integer.get()))
    num = int(integer.get())
    tries = num
    n = 1
    while n <= (((int(tries)+1)*2)):
        time.sleep(.25)
        if num == 89:
            print('No')
            happy_field.set('No')
            break
        elif num != 1:
            num = digitssquared(str(num))
        else:
            print('Happy')
            happy_field.set('Yes')
            break
        n += 1


# Build GUI
def main():
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()