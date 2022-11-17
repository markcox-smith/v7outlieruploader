import os
import sqlite3
import numpy as np
import time
import requests

from PIL import Image, ImageStat
from darwin.client import Client
from darwin.dataset.upload_manager import LocalFile, UploadHandler

item_path = 'path/to/file.jpeg'

API_KEY = "<API KEY>"

def add_files(item_path) -> None:
    """
    Adds stats of a file to the bikelanes database.
    """
    # Load image
    im = Image.open(item_path)
    item_name = os.path.basename(item_path)

    # Calculate statistics
    stats = ImageStat.Stat(im)                                                                 

    for band,name in enumerate(im.getbands()):
        if name == 'R': 
            name, rmin, rmax, rstddev, rmean = name, stats.extrema[band][0], stats.extrema[band][1], stats.stddev[band], stats.mean[band]
        if name == 'G':
            name, gmin, gmax, gstddev, gmean = name, stats.extrema[band][0], stats.extrema[band][1], stats.stddev[band], stats.mean[band]
        if name == 'B':
            name, bmin, bmax, bstddev, bmean = name, stats.extrema[band][0], stats.extrema[band][1], stats.stddev[band], stats.mean[band]

    #Importing stats into database
    conn = sqlite3.connect('bikelanes.db')

    c = conn.cursor()

    exists = c.execute(f"""SELECT COUNT(1) FROM bikelanes WHERE name = '{item_name}'""")

    if exists.fetchall()[0][0]:
        print("File already added to the dataset")
        exists = c.execute(f"""SELECT COUNT(1) FROM bikelanes WHERE name = '{item_name}'""")
    
    else:
        print("Adding new item")
        c.execute(f"""INSERT INTO bikelanes VALUES ('{item_name}',{rmin},{rmax},{rstddev},{rmean},{gmin},{gmax},{gstddev},{gmean},{bmin},{bmax},{bstddev},{bmean})""")

    conn.commit()

    conn.close()


def is_outlier(item_path) -> str:
    """
    Determines whether a file is an outlier or not based on the stats table.
    Returns a flag 'outlier' for an outlier and 'normal' otherwise.
    """
    # Load image
    im = Image.open(item_path)
    item_name = os.path.basename(item_path)

    # Calculate statistics
    stats = ImageStat.Stat(im)                                                                 

    for band,name in enumerate(im.getbands()):
        if name == 'R': 
            name, rmin, rmax, rstddev, rmean = name, stats.extrema[band][0], stats.extrema[band][1], stats.stddev[band], stats.mean[band]
        if name == 'G':
            name, gmin, gmax, gstddev, gmean = name, stats.extrema[band][0], stats.extrema[band][1], stats.stddev[band], stats.mean[band]
        if name == 'B':
            name, bmin, bmax, bstddev, bmean = name, stats.extrema[band][0], stats.extrema[band][1], stats.stddev[band], stats.mean[band]

    item_list = [rmin,rmax,rstddev,rmean,gmin,gmax,gstddev,gmean,bmin,bmax,bstddev,bmean]

    #Importing stats into database
    conn = sqlite3.connect('bikelanes.db')

    c = conn.cursor()
    std_list = []
    mean_list = []

    columns_list = ['rmin','rmax','rstddev','rmean','gmin','gmax','gstddev','gmean','bmin','bmax','bstddev','bmean']
    for col in columns_list:
        c.execute(f"""SELECT {col} FROM bikelanes""")
        stats_list = c.fetchall()
        nump_list = []
        for stat in stats_list:
            nump_list.append(stat[0])

        nst = np.std(nump_list)
        nme = np.mean(nump_list)
        std_list.append(nst)
        mean_list.append(nme)

    dev2nd = map(lambda x: x*2, std_list)
    dev2nd = list(dev2nd)

    new_list = np.subtract(mean_list,item_list)
    new_list = list(new_list)
    new_list = map(return_abs, new_list)
    new_list = list(new_list)

    check_list = np.subtract(dev2nd,new_list)
    check_list = list(check_list)

    #Filters for anything outside of 2sigma
    if check_outlier(check_list):
        flag = 'outlier'

    else:
        flag = 'normal'

    conn.commit()
    conn.close()
    return flag



#Helper Functions
def stats_generator(stats_list):
    """
    Receives a list of stats and generates stats based on it
    """
    pass

def return_abs(n):
    return abs(n)

def check_outlier(list1):
    return(all(x > 0 for x in list1))



#DB and Stats Driver Code
add_files(item_path)
flag = is_outlier(item_path)




#Uploading Files to V7
def upload_outlier(file) -> None:
    client = Client.from_api_key(API_KEY)
    dataset = client.get_remote_dataset("team-slug/dataset-slug")


    # Point to the files you wish to upload.
    local_files = [
    LocalFile(item_path, path="/", tags=["Outlier"])
    ]

    # Upload your files to your remote dataset.
    handler: UploadHandler = dataset.push(local_files)

def upload_normal(file) -> None:
    client = Client.from_api_key(API_KEY)
    dataset = client.get_remote_dataset("team-slug/dataset-slug")


    # Point to the files you wish to upload.
    local_files = [
    LocalFile(item_path, path="/", tags=["Normal"])
    ]

    # Upload your files to your remote dataset.
    handler: UploadHandler = dataset.push(local_files)


#Upload Tag API Function
def outlier_tag(item_name) -> None:

    url = "https://darwin.v7labs.com/api/v2/teams/<team-slug>/items/slots/tags"

    payload = {
        "filters": {
            "dataset_ids": [<dataset id>],
            "item_name_contains": f"{item_name}"
        },
        "annotation_class_id": <outlier tag annotation class id>
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        f"Authorization": "ApiKey {API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)


def normal_tag(item_name) -> None:

    url = "https://darwin.v7labs.com/api/v2/teams/clever-name/items/slots/tags"

    payload = {
        "filters": {
            "dataset_ids": [<dataset id>],
            "item_name_contains": f"{item_name}"
        },
        "annotation_class_id": <normal tag annotation class id>
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        f"Authorization": "ApiKey {API_KEY}"
    }

    response = requests.post(url, json=payload, headers=headers)


item_name = os.path.basename(item_path)

#Driver Code for Upload
if flag == 'outlier':
    print("Outlier")
    upload_outlier(item_path)
    time.sleep(5)
    outlier_tag(item_name)

elif flag == 'normal':
    print("Normal")
    upload_normal(item_path)
    time.sleep(5)
    normal_tag(item_name)

else:
    print("Something went wrong")
