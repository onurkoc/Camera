#!usr/bin/env python3

from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess

# Kill gphoto2 process that
# starts whenever we connect the
# camera


def killgphoto2Process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    # Search for the line that has the process
    # we want to kill

    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            # Kill the process!
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)
            print('gphoto2 process with PID:{} terminated'.format(pid))


shot_date = datetime.now().strftime("%Y-%m-%d")
shot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID = "PiShots"

clearCommand = ["--folder", "/store_00020001/DCIM/100CANON",
                "-R", "--delete-all-files"]
triggerCommand = ["--trigger-capture"]
downloadCommand = ["--get-all-files"]

folder_name = shot_date + picID
save_location = "/home/pi/Desktop/gphoto/images/" + folder_name


def createSaveFolder():
    try:
        os.makedirs(save_location)
    except:
        print("Failed to create the new directory.")
    os.chdir(save_location)


def captureImages():
    gp(triggerCommand)
    sleep(3)
    gp(downloadCommand)
    gp(clearCommand)


def renameFiles(ID):
    for filename in os.listdir("."):
        if len(filename) < 13:
            if filename.endswith(".JPG"):
                os.rename(filename, (shot_time + ID + ".JPG"))
                print("Renamed the JPG")
            elif filename.endswith(".CR2"):
                os.rename(filename, (shot_time + ID + ".CR2"))
                print("Renamed the CR2")


if __name__ == '__main__':
    killgphoto2Process()
    gp(clearCommand)
    # for time lapse enter here a while loop
    # don't forget to rename the file name otherwise photos
    # will be overwritten
    createSaveFolder()
    captureImages()
    renameFiles(picID)
