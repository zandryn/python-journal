'''
    WORD PROBLEM:
    You are given the following information, but you may prefer to do some research for yourself.

    1 Jan 1900 was a Monday.
    Thirty days has September,
    April, June and November.
    All the rest have thirty-one,
    Saving February alone,
    Which has twenty-eight, rain or shine.
    And on leap years, twenty-nine.
    A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
    How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?

'''

def count_sundays(date1, date2):
    day_counter = { 'monday' : 0, 'tuesday' : 0, 'wednesday' : 0, 'thursday' : 0, 'friday' : 0, 'saturday' : 0, 'sunday' : 0 }

    print("Dates: ", date1, date2, "\n")
    print(day_counter, "\n")

    days = 0
    start = 'monday'

    while date1 != date2:
        if date1[2] == 2:                           # if FEB then 28 days
            if date1[3] % 400 and date1[3] % 4:     # leap year
                days = 29
            else:                                 # not leap year
                days = 28
        elif date1[2] == 4 or date1[2] == 6 or date1[2] == 9 or date1[2] == 11:
            days = 30
        else:
            days = 31
        print(days)

        for i in range(1, days + 1):
            print(i, end='-')
            match date1[1]:
                case 1:
                    c

        break

# day - month - year
date1 = [1, 1, 1900]
date2 = [31, 12, 2000]

count_sundays(date1, date2)