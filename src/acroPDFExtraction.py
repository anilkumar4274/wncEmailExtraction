import json
import PyPDF2 as pypdf
import os
import re
import utilities

#fileName = 'D:\\WNC\\Email_extraction\\email_data\\WNCDataExtraction_v7\\output\\2021-11-10_2207 Corrected Worksheet Primary Flood Quote Request - Robert Poiner\\R_Poiner - WNC NY Flood Quote Request.pdf'
def extractAcroPdfData(fileName, editPDFCount = 0, nonEditPDFCount = 0):
    acro_data = ""
    try:
        pdfobject=open(fileName,'rb')
        pdf=pypdf.PdfFileReader(pdfobject)
        acro_data = pdf.getFormTextFields()
        if acro_data in ["", {}, "{}"]:
            raise Exception('Not Editable PDF')
        print("Editable PDF Path - ", fileName)
        editPDFCount = editPDFCount + 1
    except:
        pdfobject.close()
        nonEditPDFCount = nonEditPDFCount + 1
        filePath = fileName.replace(fileName.split("/")[-1].split("\\")[-1], "")
        newFileName = (filePath + "NE_" + fileName.split("/")[-1].split("\\")[-1])
        os.rename(fileName, newFileName)
        print("Acrobat exception")

    if not acro_data in ["", {}, "{}"]:
        try:
            output_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))+ "\\output\\"
            utilities.createFolder(output_directory + "/attachmentOutput")
        except(UnicodeEncodeError, AttributeError, TypeError, FileNotFoundError) as e:
            print("Creating Folder exception --- ", e)

        try:
            output_directory = output_directory + "/attachmentOutput/"
            json_file = fileName.split("\\")[-1].split("/")[-1].split(".")[0:-1]
            json_file = "".join(json_file).lower().replace(" ","")
            json_file = "".join(re.findall('[0-9a-z]', json_file))

            with open(output_directory + json_file + '.json', 'w') as fp:
                json.dump(acro_data, fp)
        except(UnicodeEncodeError, AttributeError, TypeError, FileNotFoundError) as e:
            print("Editable PDF json exception --- ", e)

    return editPDFCount, nonEditPDFCount

#extractAcroPdfData(fileName)



