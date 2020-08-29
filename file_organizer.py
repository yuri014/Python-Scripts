import time
import os
import glob
import schedule

files_list = glob.glob("*")

extension_files = set()

for file in files_list:
    extension = file.split(sep=".")
    try:
        if not file.endswith('.py'):
            extension_files.add(extension[1])
    except IndexError:
        continue


def createDirectory():
    for dir in extension_files:
        try:
            os.makedirs(dir+"_files")
        except FileExistsError:
            continue


def arrange():
    for file in files_list:
        arrange_extension = file.split(sep=".")
        try:

            os.rename(file, arrange_extension[1] + "_files/" + file)
        except (OSError, IndexError):
            continue


def calls():
    createDirectory()
    arrange()


schedule.every(20).minutes.do(calls)

while True:
    schedule.run_pending()
    time.sleep(1)
