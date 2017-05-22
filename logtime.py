#!/usr/bin/env python


# Usage
#
# 1. Put this file on your path.
# 1. Add `alias lt="logtime.py` to your `bash.bashrc` file
#
# To log time: Type `lt "thing"` into your bash shell
# To open your daily log file:  type or `lt`


import os
import sys
import re
import string
from datetime import date, datetime


def _formatEntry(previousTimeEntry, timeEntry, taskEntry, taskLength):
    return "|\t" + str(previousTimeEntry) + "\t|\t" + str(timeEntry) + "\t|\t" + str(taskEntry) + "\t|\t" + str(taskLength) + "\t|\n"


def _getFirstTimeEntry(entryLine):
    match = re.findall("([0-1]*[0-9]:[0-6][0-9] [AP]M)", entryLine)
    if match:
        return match[0]
    else:
        return None


def _getSecondTimeEntry(entryLine):
    match = re.findall("([0-1]*[0-9]:[0-6][0-9] [AP]M)", entryLine)
    if match:
        return match[1]
    else:
        return None


def _convertTimeOfDay(timeOfDay):
    if timeOfDay == 'A' or timeOfDay == 'a':
        return "AM"
    if timeOfDay == 'P' or timeOfDay == 'p':
        return "PM"
    return None


def _getTimeFromArgument(argTime):
    timeStamp = re.findall("([0-1]*[0-9]:[0-6][0-9])", argTime)
    timeOfDay = re.findall("[AaPp]", argTime)
    if not timeStamp or not timeOfDay:
        return None
    if _convertTimeOfDay(timeOfDay[0]):
        return str(timeStamp[0]) + " " + str(_convertTimeOfDay(timeOfDay[0]))
    else:
        return None


def _getLengthBetweenTimes(previousTimeEntry, timeEntry):
    d1 = datetime.strptime(previousTimeEntry, "%I:%M %p")
    d2 = datetime.strptime(timeEntry, "%I:%M %p")
    return (d2 - d1).total_seconds() / 3600


def _updateLengthBetweenTimes(filePath):
    f = open(filePath, "r")
    readLines = f.readlines()
    f.close()
    f = open(filePath, "w")
    for currentLine in readLines:
        firstTimeEntry = _getFirstTimeEntry(currentLine)
        if firstTimeEntry:
            secondTimeEntry = _getSecondTimeEntry(currentLine)
            items = string.split(currentLine, "|")
            f.write(_formatEntry(items[1].strip(), items[2].strip(), items[3].strip(), _getLengthBetweenTimes(firstTimeEntry, secondTimeEntry)))
        else:
            f.write(currentLine)
    f.close()


def _getFilePath():
    #Always reset path to this file
    if os.path.isdir(sys.path[0]):
        os.chdir(sys.path[0])
    else:
        os.chdir(os.path.dirname(sys.path[0]))

    logFileDirectory = "time-log-files"

    if not os.path.exists(logFileDirectory):
        os.mkdir(logFileDirectory)

    currentDate = date.today().isoformat()
    filePath = logFileDirectory + "/" + currentDate + ".md"

    if not os.path.isfile(filePath):
        f = open(filePath, "a+")
        f.write("# Notes:\n\n")
        f.write("Administration: admin\n")
        f.write("Work: wk\n")
        f.write("Side Project: sd\n")
        f.write("Scrum: scm\n")
        f.write("Peer Review: pr\n\n")
        f.write("# Time log:\n\n")
        f.write(_formatEntry("Start", "End", "Task", "Length"))
        f.write(_formatEntry("---", "---", "---", "---"))
        f.close()

    return filePath


def _printLastLineToConsole(filePath):
    f = open(filePath, "a+")
    lines = f.readlines()
    print lines[len(lines)-1]
    f.close()


filePath = _getFilePath()

if len(sys.argv) < 2:
    os.system("start " + filePath)
    exit()

_updateLengthBetweenTimes(filePath)

f = open(filePath, "a+")
lines = f.readlines()
lastTimeEntry = _getSecondTimeEntry(lines[len(lines)-1])
currentTimeEntry = datetime.today().time().strftime("%I:%M %p")
taskEntry = " ".join(sys.argv[1:])

if len(sys.argv) > 2:
    firstTimeArg = _getTimeFromArgument(sys.argv[1])
    secondTimeArg = _getTimeFromArgument(sys.argv[2])
    if firstTimeArg and secondTimeArg:
        lastTimeEntry = firstTimeArg
        currentTimeEntry = secondTimeArg
        taskEntry = " ".join(sys.argv[3:])
    elif firstTimeArg:
        currentTimeEntry = firstTimeArg
        taskEntry = " ".join(sys.argv[2:])

if lastTimeEntry:
    f.write(_formatEntry(lastTimeEntry, currentTimeEntry, taskEntry, _getLengthBetweenTimes(lastTimeEntry, currentTimeEntry)))
else:
    startTime = "07:00 AM"
    f.write(_formatEntry(startTime, currentTimeEntry, taskEntry, _getLengthBetweenTimes(startTime, currentTimeEntry)))
f.close()

_printLastLineToConsole(filePath)
