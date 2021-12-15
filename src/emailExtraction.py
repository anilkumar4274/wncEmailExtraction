import emlExtraction
import msgExtraction
import os

def msg_file_extraction(data_directory):
    try:
        msgExtraction.mail_content_extraction(data_directory, ".msg")
    except(UnicodeEncodeError, AttributeError, TypeError) as e:
        print("--> ", e)

def eml_file_extraction(data_directory, output_directory):
    for mail in os.listdir(data_directory):
        try:
            if mail.endswith(".eml"):
                folder_name = mail.split(".")[0]
                msg = emlExtraction.parse_message(data_directory+mail)
                attachments = emlExtraction.find_attachments(msg)
                emlExtraction.download_attachments(data_directory + mail, output_directory + folder_name)

                text = emlExtraction.extract_mail_body(data_directory+mail)
                file = open(output_directory + folder_name + "\emailData.txt", "w")
                file.write(text)

                file.close()

        except(UnicodeEncodeError, AttributeError, TypeError) as e:
            print("--> ", e)