import shutil
import utilities

def classifyEmails(data_directory):
    for file in utilities.get_all_filepaths(data_directory):
        try:
            if file.endswith(".eml"):
                shutil.move(file, data_directory + "/eml/" + file.split("\\")[-1].split("/")[-1])
            elif file.endswith(".msg"):
                shutil.move(file, data_directory + "/msg/" + file.split("\\")[-1].split("/")[-1])

        except(UnicodeEncodeError, AttributeError, TypeError, FileNotFoundError) as e:
            ext = file.split(".")[-1]
            utilities.createFolder(data_directory + "/" + ext)
            classifyEmails(data_directory)
            print("--> ", e)
            break

