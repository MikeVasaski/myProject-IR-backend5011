# Python program to delete a csv file
# csv file present in same directory
import os

# first check whether file exists or not
# calling remove method to delete the csv file
# in remove method you need to pass file name and type


def remove_file():
    file = '../resources/anime.csv'

    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
        print("file deleted")
    else:
        print("file not found")
