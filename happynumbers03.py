#!python
# File happynumbers.py

"""
Starting with any positive integer, replace the number by the sum of the squares of its digits, and repeat the process
until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
Those numbers for which this process ends in 1 are happy numbers, while those that do not end in 1 are unhappy numbers.
"""

import time
from tkinter import *
from tkinter import ttk


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
root = Tk()
root.geometry("320x180")
root.title("Happy Numbers")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

integer = StringVar()
happy_field = StringVar()

integer_entry = ttk.Entry(mainframe, width=7, textvariable=integer)
integer_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=happy_field).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=happy).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="Enter integer:").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Is it Happy?").grid(column=1, row=2, sticky=E)

# p = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=200, mode='determinate', maximum=100)
# p.grid(column=2, row=4)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

integer_entry.focus()
root.bind('<Return>', happy)

root.mainloop()
