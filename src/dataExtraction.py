import os
import utilities
import classifyEmail
import emailExtraction
import acroPDFExtraction

path = os.getcwd()
data_directory = os.path.abspath(os.path.join(path, os.pardir)).replace("\\","/") + "/data/"
output_directory = os.path.abspath(os.path.join(path, os.pardir)).replace("\\","/") + "/output/"

#Unzip Files
utilities.unzipFiles(data_directory, "sample_emails.zip")
utilities.unzipFiles(data_directory, "sample_emails_v2.zip")
utilities.unzipFiles(data_directory, "sample_emails_v3.zip")

# Classify the .eml and .msg file
classifyEmail.classifyEmails(data_directory)

# Extract data from emails and download attachments to respective folders
list_data_subfolders = [f.name for f in os.scandir(data_directory) if f.is_dir()]

for sub_dir in list_data_subfolders:
    directory = data_directory + sub_dir + "/"
    if sub_dir == "msg":
        emailExtraction.msg_file_extraction(directory)
    elif sub_dir == "eml":
        emailExtraction.eml_file_extraction(directory, output_directory)

#Convert Unstructured json to structured json and remove unstructured json file
utilities.convertJsonToStructuredFormat(output_directory)

#Extract data from the Acrobat PDF
subDirs, files = utilities.getSubDirectoriesAndFiles(output_directory)
ind = 0
paths = []

try:
    for subDir in subDirs:
        for file in files[ind]:
            paths.append(output_directory+subDir+"/"+file)
        ind = ind+1
    print(paths)
except(UnicodeEncodeError, AttributeError, TypeError, FileNotFoundError) as e:
    print("exception --- ", e)

for path in paths:
    try:
        if path.endswith(".pdf"):
            acroPDFExtraction.extractAcroPdfData(path)
    except(UnicodeEncodeError, AttributeError, TypeError, FileNotFoundError) as e:
        print("exception --- ", e)


