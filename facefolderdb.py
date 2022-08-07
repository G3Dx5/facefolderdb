#!/usr/bin/env python3

"""
Perform facial recognition (matching) against corpus of known face images using "face_recognition" library

Use / Paramaters:
    python3 scriptname -i <imagename_of_unknown> -s source_directory
    eg. python3 facefolderdb.py -i unknown_face.jpg -s image_files
    Todo:   
            - hash the images and store to the database 
            - check if the unknown is in the database first (after hash added to database) If hash found print "already found"
            - create a new folder / file structure for each run 
            - args for the destination folder 
"""

import argparse
import datetime
from dbhandler import Createdb
import face_recognition
import glob
import hashlib
import os
import shutil
from time import sleep, time
from PIL import Image, ImageDraw, ImageFont
import sqlite3
from timewatch import timelogger
import resizing

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file")
parser.add_argument("-s", "--source", help="image source files")
args = parser.parse_args()

MASTER = args.input
source_loc = args.source
images = os.listdir(args.source)

finds = []

def getFileHash(image, hash_func):
    with open(image, 'rb') as f:
        return hash_func(f.read()).hexdigest()

def checkMasterhash(MASTER):
    master_hash = getFileHash(MASTER, hashlib.md5)
    ''' check the database and see if the master has been seen before proceeding '''
    print(master_hash)


class Filechecker():
    ''' check files are correct types and remove invalid files (skip .DS files) '''
    def file_type_check(self):
        for photo in images:
            if photo != '.DS_Store':
                filename, *middle, extension = photo.split(".")
                if extension == 'jpg':
                    continue
                else:
                    shutil.move("images/" + photo, "invalid/")
                    print("File " + photo + " not a valid image type. Moving to invalid files directory")

class Facefolder(Filechecker):
    ''' check and match master face against corpus folder of faces'''
    @timelogger
    def facefolder(self):
        print("\nMATCHING FACES TO {} .....\n".format(MASTER))
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        time = datetime.datetime.now().strftime("%H%M" + "hrs")
        image_to_be_matched = face_recognition.load_image_file(MASTER)
        image_to_be_matched_encoded = face_recognition.face_encodings(image_to_be_matched)[0]
        for image in images:
            current_image = face_recognition.load_image_file("images/" + image)
            current_image_encoding = face_recognition.face_encodings(current_image)
            if len(current_image_encoding) > 0:
                current_image_encoding = current_image_encoding[0]
                result = face_recognition.compare_faces([image_to_be_matched_encoded], current_image_encoding)
                if result[0] == True:
                    match = "MATCH"
                    # hash_target = str(source_loc) + "/" + str(image)
                    # result_hash = getFileHash(hash_target, hashlib.md5)
                    found_elements = (date, time, match, image, MASTER)
                    finds.append(found_elements)
                    print("MATCH: " + image + " to " + MASTER)
                    shutil.copy2(os.path.join("./images", image), "success")
                else:
                    print("Not matched: " + image)

    def dbadd(self):
        ''' Add matches to the database '''
        print("\nADDING MATCHES TO THE DATABASE...\n")
        for result in finds:
            date, time, match, image, MASTER = result
        conn = sqlite3.connect('facematch.db')
        curs = conn.cursor()
        match = 'MATCH'
        curs.executemany('insert into matches (date, time, match, filemaster, filecompared) values (?,?,?,?,?)', finds)
        conn.commit()
        conn.close()

class ImageFolder:
    ''' loop through images in match folder and create composite with master image on LHS'''
    def create_composites(self):
        with Image.open(MASTER) as master:
            width, height = master.size
            success_images = glob.glob("success/*.jpg")
            save_path = "combos/"
            print("\nCREATING COMPOSITE IMAGES....")
            for image in success_images:
                with open(image, 'rb') as matched_image:
                    iname = os.path.splitext(os.path.basename(image))[0]
                    matched_image = Image.open(image)
                    # master_width_percent = (width/float(master.size[0]))
                    # master_horizontal_size = int((float(master.size[1])*float(master_width_percent)))
                    # matched_image = matched_image.resize((width, master_horizontal_size), Image.ANTIALIAS)
                    WIDTH = master.size[0] + matched_image.size[0]
                    HEIGHT = master.size[1]
                    new_image = Image.new("RGB", (WIDTH, HEIGHT))
                    new_image.paste(master, (0, 0))
                    new_image.paste(matched_image, (master.size[0], 0))
                    date = datetime.datetime.now().strftime("%d%m%Y")
                    time = datetime.datetime.now().strftime("%H%M%S" + "hrs")
                    new_image.save(save_path + date + " " + time + " " + str(MASTER) +  " to " + str(iname) + ".jpg") 
                    sleep(1.5)


class Dbshow():
    ''' Dump out the database matches '''
    def dbshow(self):
        conn = sqlite3.connect('facematch.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM matches")
        res = curs.fetchall()
        for result in res:
            print(result[0], result[1], result[2], result[3], result[4])
        conn.commit()
        conn.close()

def results_stats():
    total = len(os.listdir('./images'))
    wins = len(os.listdir("success"))
    invalids = len(os.listdir('./invalid'))
    print("FILES ANALYSED: " + str(total))
    print("MATCHES DETECTED: " + str(wins -1))
    print("INVALID FILES (not analysed): " + str(invalids))

if __name__ == "__main__":
    ff = Facefolder()
    ff.facefolder()
    ff.dbadd()
    i = ImageFolder()
    i.create_composites()
    Dbshow().dbshow()
    results_stats()
