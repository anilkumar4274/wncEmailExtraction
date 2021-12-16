import os
import re
import json
import zipfile
from collections import Iterable

def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item

#Remove file from the path
def remove_file(filename):
    os.remove(filename)

#Convert unordered json format to formatted json format
def convertJsonToStructuredFormat(directory):
    dictionary = [f.path for f in os.scandir(directory) if f.is_dir()]
    for dict in  dictionary:
        try:
            with open(dict + "/message.json") as json_file:
                data = json.load(json_file)

            json_file = dict.split("\\")[-1].split("/")[-1]
            json_file = "".join(json_file).lower().replace(" ", "")
            json_file = "".join(re.findall('[0-9a-z]', json_file))
            createFolder(os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace("\\","/") +"/output/emailOutput")
            with open(os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace("\\","/") + "/output/emailOutput/"+json_file+".json", "w") as outfile:
                json.dump(data, outfile, indent=3)

        except(UnicodeEncodeError, AttributeError, TypeError, FileNotFoundError) as e:
            print("exception --- ", e)

        try:
            remove_file(dict+"/message.json")
        except(UnicodeEncodeError, AttributeError, TypeError, FileNotFoundError) as e:
            print("exception --- ", e)

#Get all Sub directories and files in it
def getSubDirectoriesAndFiles(directory):
    filesLst = []
    subDirectories = []

    for subdir, dirs, files in os.walk(directory):
        if len(dirs) > 0:
            subDirectories = dirs
        filesLst.append(files)
    return subDirectories, filesLst[1:]

def get_all_filepaths(root_path):
    for root, dirs, files in os.walk(root_path):
        for filename in files:
            yield os.path.join(root, filename)

#Create Folder
def createFolder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

#Unzip files
def unzipFiles(data_directory, file_name):
    try:
        with zipfile.ZipFile(data_directory+file_name, 'r',allowZip64=True) as zip_ref:
            zip_ref.extractall(data_directory)
    except(UnicodeEncodeError, AttributeError, TypeError, FileNotFoundError) as e:
        print("exception --- ", e)

#Get count of files as per extensions
def getCountOfFiles(directory):
    extensionsList = []
    attachmentCount = dict()
    for file in get_all_filepaths(directory):
        extensionsList.append(file.split(".")[-1].lower())

    for ext in set(extensionsList):
        attachmentCount[ext] = extensionsList.count(ext)

    return attachmentCount