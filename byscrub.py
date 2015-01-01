__author__ = 'philipp'
from subprocess import Popen, PIPE
import time
import os
#### Config
logPath = "/var/log/byscrub.log"

#### Functions
def sendmail(event, subject, message):
    p = Popen(["/usr/bin/gymail.py", "-e", event, "-s", subject, "-m", message], stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()

def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)

def findBtrfsMounts():
    btrfsRootSubvolList = list()
    mpointsWithoutBtrfsTrashbinList = list()
    for line in open("/proc/mounts", "r"):
        mountLineList = line.split(" ")
        if "btrfs" in mountLineList[2]:
            btrfsRootSubvolList.append(mountLineList[1])
    return btrfsRootSubvolList

def log(event, btrfsMount, msg):
    tstamp = str(int(time.time()))
    with open(logPath, "a") as myfile:
        myfile.write("\n%s: time: %s, btrfs-mount: %s\n%s" % (event, tstamp, btrfsMount, msg))

#### Main
for btrfsMount in findBtrfsMounts():
    print("Started btrfs scrub for %s"   % btrfsMount)
    p1 = Popen(["btrfs", "scrub", "start", "-B", "-d", btrfsMount], stdout=PIPE, stderr=PIPE)
    out, err = p1.communicate()
    outd = out.decode('utf-8')
    errd = err.decode('utf-8')
    print(outd)
    if "with 0 errors" in outd:
        print("all fine")
        log("(INFO)", btrfsMount, "\tout: %s\terr: %s" % (outd, errd))
    else:
        sendmail("error", "byscrub error: %s" % btrfsMount,
                 "byscrub error %s:\n  out: %s \n err: %s" % (btrfsMount, outd, errd))
        log("(EE)", btrfsMount, "\tout: %s\terr: %s" % (outd, errd))

