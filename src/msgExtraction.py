import extract_msg
import os
import pandas as pd

#Create separate folder by email name and extract data from email like from, to, cc, subject, date, mail body and attachments will be downloaded
def mail_content_extraction(directory,extension):
    for mail in os.listdir(directory):
        try:
            if mail.endswith(extension):
                msg = extract_msg.Message(directory + mail)
                msg.save(customPath=os.path.abspath(os.path.join(os.getcwd(), os.pardir)).replace("\\","/")+"/output/", toJson="emailData.json")
        except(UnicodeEncodeError,AttributeError,TypeError, FileNotFoundError) as e:
            print("--> ", e)

#Import the data to Python DataFrame using the extract_msg module
def DataImporter(directory, extension):
    my_list = []
    for mail in os.listdir(directory):
        try:
            if mail.endswith(extension):
                msg = extract_msg.Message(directory+mail)
                my_list.append([msg.filename,msg.sender,msg.to, msg.date, msg.subject, msg.body]) #These are in-built features of 'extract_msg.Message' class
                global df
                df = pd.DataFrame(my_list, columns = ['File Name','From','To','Date','Subject','MailBody'])
        except(UnicodeEncodeError,AttributeError,TypeError,FileNotFoundError) as e:
            print("--> ",e)
    return df
