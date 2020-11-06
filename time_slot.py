import json
import re
import datetime
from datetime import timedelta
from datetime import time
import os
from os import listdir


class Time:
    def __init__(self, hrs, mins, phase):
        self.hrs = hrs
        self.mins = mins
        self.phase = phase


def sanitize_time(time):
    total_mins = 0
    if(time.phase == "AM"):
        total_mins = total_mins+(int(time.hrs) - 9)*60
        total_mins = total_mins+(int(time.mins))
    elif(time.phase == "PM"):
        total_mins = total_mins+(int(time.hrs) + 3)*60
        total_mins = total_mins+(int(time.mins))
    return total_mins


def fill_empty(filled_slots):
    empty_slots = []
    if(filled_slots[0][0].hrs == "9" and filled_slots[0][0].mins == "00"):
        pass
    else:
        temp = Time("9", "00", "AM")
        empty_slots.append([temp, filled_slots[0][0]])

    for i in range(0, len(filled_slots)-1):

        if(not((filled_slots[i][1].hrs == filled_slots[i+1][0].hrs) and (filled_slots[i][1].mins == filled_slots[i+1][0].mins))):
            if(filled_slots[i][1].hrs == "12"):
                temp1 = Time(filled_slots[i][1].hrs,
                             filled_slots[i][1].mins, "PM")
            else:
                temp1 = Time(
                    filled_slots[i][1].hrs, filled_slots[i][1].mins, filled_slots[i][1].phase)

            if(filled_slots[i+1][0].hrs == "12"):
                temp2 = Time(filled_slots[i+1][0].hrs,
                             filled_slots[i+1][0].mins, "PM")
            else:
                temp2 = Time(
                    filled_slots[i+1][0].hrs, filled_slots[i+1][0].mins, filled_slots[i+1][0].phase)

            empty_slots.append([temp1, temp2])

    if(filled_slots[len(filled_slots)-1][1].hrs == "5" and filled_slots[len(filled_slots)-1][1].mins == "00"):
        pass
    else:
        temp = Time("5", "00", "PM")
        empty_slots.append([filled_slots[len(filled_slots)-1][1], temp])

    return empty_slots


def fill_time_1(t1, t2):
    t1o = sanitize_time(t1)
    t2o = sanitize_time(t2)
    for i in range(t1o, t2o):
        buckets1[i] = 1


def fill_time_2(t1, t2):
    t1o = sanitize_time(t1)
    t2o = sanitize_time(t2)
    for i in range(t1o, t2o):
        buckets2[i] = 1


def rev_sanitize(mins):
    h = mins/60
    rm = mins % 60
    if (rm <= 9):
        rm = "0"+str(rm)

    if(h >= 3):
        if(h >= 4):
            tt = Time(int(9+h-12), rm, "PM")
        else:
            tt = Time(int(9+h), rm, "PM")
    else:
        tt = Time(int(9+h), rm, "AM")

    return tt

def get_common_array(all_free_slots,nooffiles,duration):
    finalcounter = 0
    for i in range (0,480):
        
        counter=0
        for j in range (0,nooffiles-1):
            if(all_free_slots[j][i]== 0 and all_free_slots[j+1][i]==0):
                counter=counter+1
            else:
                counter = 0    
        
        if(counter == nooffiles-1):
            finalcounter = finalcounter+1    
        else:
            finalcounter = 0

        if(finalcounter== duration):
            p = rev_sanitize(i+1)
            t = rev_sanitize(i-duration+1)
            strp = ""
            strp += str(t.hrs)+":"+str(t.mins)+str(t.phase)+" "+"-" + \
            " "+str(p.hrs)+":"+str(p.mins)+str(p.phase)
            return strp
    return "No common slot"

def get_common(duration, a1, a2):
    cntr = 0
    index = 0
    for i in range(0, 480):
        if(a1[i] == 0 and a2[i] == 0):
            cntr = cntr+1
            if(cntr == duration):
                index = i-cntr
                break
        else:
            cntr = 0

    if(cntr < duration):
        print("No slot available")
        return None
    else:
        t = rev_sanitize(index+1)
        p = rev_sanitize(index+duration+1)
        strp = ""
        strp += str(t.hrs)+":"+str(t.mins)+str(t.phase)+" "+"-" + \
            " "+str(p.hrs)+":"+str(p.mins)+str(p.phase)

        return strp


arr = os.listdir('./Employees')

#f1 = open(arr[0], "r")
all_free_slots = []
print (arr)
numberoffiles = len(arr)
for file in arr:
    f1 = open("./Employees/"+file, "r")
    line1 = f1.readline()


    obj1 = eval("(" + line1 + ")")


    keys_employee = []
    for key in obj1.keys():
        keys_employee.append(key)


    a = (obj1[keys_employee[0]].keys())

    for key1 in a :
        date1 = key1
    access1 = obj1[keys_employee[0]][date1]
    

    time1 = []
    buckets1 = [0] * 480  # 480 mins  = 8 hrs

    for item in access1:
        item = item.replace(" ", "")
        x = re.search(
            "^(1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm])(-)(1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm])$", item)

        t1 = Time(x.group(1), x.group(2), x.group(3))
        if(t1.hrs == "12"):
            t1.phase = "AM"

        t2 = Time(x.group(5), x.group(6), x.group(7))
        if(t2.hrs == "12"):
            t2.phase = "AM"

        time1.append([t1, t2])

        fill_time_1(t1, t2)

    all_free_slots.append(buckets1)


    empty1 = fill_empty(time1)


    str1 = ""

    for i in range(0, len(empty1)):
        str1 += "'"+empty1[i][0].hrs+":"+empty1[i][0].mins+" "+empty1[i][0].phase + \
            " - "+empty1[i][1].hrs+":"+empty1[i][1].mins + \
                " "+empty1[i][1].phase+"'"+","






    file1write = open("output.txt", "a")

    file1write.write("\nAvailable slot \n")
    file1write.write("Employee1: [")
    file1write.write(str1)
    file1write.write("]")
    file1write.write("\n")
    

    # file1write.write(strh)
    file1write.close()

    

print(get_common_array(all_free_slots,numberoffiles,1))


#time = input("Enter slot duration in hours : ")
#strh = get_common(int(float(time)*60), buckets1, buckets2)