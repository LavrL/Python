#!/usr/bin/python
import boto3
import logging
import sys
import urllib2
import os
import datetime
from datetime import datetime, timedelta
import time
import boto
from boto.ec2 import connect_to_region

#Script for rotating AWS snapshots.
#This script does the following:
#1. Create snapshot of instance.
#2. Delete snapshot that older than n days(default 15 days)
#3. Write all information about backup process in log file

instanceid = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read()
print(instanceid)

region = urllib2.urlopen('http://169.254.169.254/latest/meta-data/placement/availability-zone').read()
region = region[:-1]
print(region)

ec2 = boto3.resource('ec2', region_name=region)

def SnapshotLogging():
    myfilename = "mylog.log"
    try:
        checkfile = os.access(myfilename,os.W_OK)
    except Exception:
        print('File does not exist')
        exit()
    else:
        file = open(myfilename,'a')
        sys.stdout = file
        print(" ")
        print(instanceid)
        print(region)
    return

def CreateBackup():
    instance = ec2.Instance(instanceid)
    print(instance)
    volumes = instance.volumes.all() # If you want to list out all volumes
    volume_ids = [v.id for v in volumes]

    for volume_id in volume_ids:
        print("Created snapshot from volume - " + volume_id)
        snapshot = ec2.create_snapshot(Description=instanceid + " - " + volume_id, VolumeId=volume_id)
	instance.create_tags(Resources=[volume_id],Tags=[{"Key": "TakenBy", "Value" : "AutomatedBackup"}])
    return

def OldSnapshotBackup():
    nDaysBefore = datetime.now() - timedelta(days=15)
    epoch = datetime.utcfromtimestamp(0)
    dateRetention=((nDaysBefore - epoch).total_seconds())

    instance = ec2.Instance(instanceid)
    volumes = instance.volumes.all() # If you want to list out all volumes
    volume_ids = [v.id for v in volumes]

    ec21 = connect_to_region(region)
    for volume_id in volume_ids:
        snapshotList = ec21.get_all_snapshots(filters={'volume-id':volume_id} )
        #print(snapshotList)
        for snapshot in snapshotList:
            #print(snapshot.start_time)
            if (snapshot.start_time < datetime.now):
                print("Deleting - " + snapshot.id)
                snapshot.delete(dry_run=False)
    return


SnapshotLogging()
CreateBackup()
OldSnapshotBackup()
