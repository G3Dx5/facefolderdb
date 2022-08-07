## facefolderdb

Perform facial recognition (matching) against corpus of known face images

Code takes an image of a face and seeks to match the image against a corpus
of faces previously obtained. The input image is first checked for type
compatability as an image file.  Matching then comences. If a match is found
the code then creates a side by side collage of the input image and the
matched image in a seperate folder for checking by the user. The program then creates an entry
in a sqlite3 database for later matching.  The time taken and time of execution
of the program is also created in a matching log file.

# Outputs: 
    - facefolder.log: log file of date / time used and time of execution. Uses  
    - facematch.db: sqlite3 database 


# Todo:   
    hash the images and store to the database 
    check if the unknown is in the database first (after hash added to database) If hash found print "already found"
    create a new folder / file structure for each run 
    args for the destination folder 


## Use / Paramaters:
    python3 scriptname -i <imagename_of_unknown> -s source_directory
    eg. python3 facefolderdb.py -i unknown_face.jpg -s image_files
