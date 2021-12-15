import json
import PyPDF2 as pypdf
import os
import re
import utilities

#fileName = 'D:\\WNC\\Email_extraction\\email_data\\WNCDataExtraction_v7\\output\\2021-11-10_2207 Corrected Worksheet Primary Flood Quote Request - Robert Poiner\\R_Poiner - WNC NY Flood Quote Request.pdf'
def extractAcroPdfData(fileName):
    pdfobject=open(fileName,'rb')
    pdf=pypdf.PdfFileReader(pdfobject)
    acro_data = pdf.getFormTextFields()
    data = pdf.getFields()
    output_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))+ "\\output\\"
    utilities.createFolder(output_directory + "/attachmentOutput")
    output_directory = output_directory + "/attachmentOutput/"
    json_file = fileName.split("\\")[-1].split("/")[-1].split(".")[0:-1]
    json_file = "".join(json_file).lower().replace(" ","")
    json_file = "".join(re.findall('[0-9a-z]', json_file))

    with open(output_directory + json_file + '.json', 'w') as fp:
        json.dump(acro_data, fp)

#extractAcroPdfData(fileName)



