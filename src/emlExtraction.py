import os
import os.path

from email.parser import Parser
from email import policy
from email.parser import BytesParser

# Opening and Parsing through the .eml file
def parse_message(filename):
    with open(filename) as f:
        return Parser().parse(f)

#Returns a tuple of parsed content-disposition dictionary, message object for each attachment found.
def find_attachments(message):
    found = []
    for part in message.walk():
        if 'content-disposition' not in part:
            continue
        cdisp = part['content-disposition'].split(';')
        cdisp = [x.strip() for x in cdisp]
        if cdisp[0].lower() != 'attachment':
            continue
        parsed = {}
        for kv in cdisp[1:]:
            key, val = kv.split('=')
            if val.startswith('"'):
                val = val.strip('"')
            elif val.startswith("'"):
                val = val.strip("'")
            parsed[key] = val
        found.append((parsed, part))
    return found

#Downloading attachments found in an .eml file
def download_attachments(eml_filename, output_dir):
    msg = parse_message(eml_filename)
    attachments = find_attachments(msg)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    for cdisp, part in attachments:
        cdisp_filename = os.path.normpath(cdisp['filename'])
        # prevent malicious crap
        if os.path.isabs(cdisp_filename):
            cdisp_filename = os.path.basename(cdisp_filename)
        towrite = os.path.join(output_dir, cdisp_filename)
        with open(towrite, 'wb') as fp:
            data = part.get_payload(decode=True)
            fp.write(data)

def extract_mail_body(eml_mail):
    with open(eml_mail, 'rb') as fp:
        mail_body = BytesParser(policy=policy.default).parse(fp)

    mail_body.get_body(preferencelist=('plain')).get_content()
    mail_body_text = mail_body.get_body(preferencelist=('plain')).get_content()
    return mail_body_text

