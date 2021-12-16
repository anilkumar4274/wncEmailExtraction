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
paths = []
editPDFCount = 0
nonEditPDFCount = 0

for filePath in utilities.get_all_filepaths(output_directory):
    paths.append(filePath)

for path in paths:
    try:
        if path.endswith(".pdf") or path.endswith(".PDF"):
            editPDFCount, nonEditPDFCount = acroPDFExtraction.extractAcroPdfData(path, editPDFCount, nonEditPDFCount)
    except(UnicodeEncodeError, AttributeError, TypeError, FileNotFoundError) as e:
        print("Acrobat exception", e)

print("editPDFCount", editPDFCount)
print("nonEditPDFCount", nonEditPDFCount)

# Get count of file types
print(utilities.getCountOfFiles(output_directory))

