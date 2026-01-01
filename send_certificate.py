from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
import argparse
from pathlib import Path
import re

argparser = argparse.ArgumentParser(description="Sends emails with certificates attached.")
argparser.add_argument('-e', '--emails', nargs='?', action='store', help="Path to the file containing the list of emails to send certificates to.",
					   default="emails.txt", required=True)
argparser.add_argument('-n', '--names', nargs='?', action='store', help="Path to the file containing the list of participant names.",
					   default="names.txt", required=False)
argparser.add_argument('-c', '--certificates', nargs='?', action='store', help="Path to the directory containing the certificates.",
					   default="pdfout", required=False)
argparser.add_argument('-s', '--subject', nargs='+', action='store', help="Subject of the email.",
					   required=True)
argparser.add_argument('-sd', '--sender', nargs='?', action='store', help="Sender's email address.",
					   required=True)
setattrs = argparser.parse_args()


### find certificate in the given path for a given name
def find_certificate(name, path):
	name_parts = re.split('\s+', name)
	for filename in os.listdir(path):
		matched = True
		for part in name_parts:
			if part not in filename:
				matched = False
				break
		if matched:
			return path / filename

print("Enter sender's mail password:")
pssw = input().strip("\n")
with open(setattrs.emails, "r") as emails_fh:
	emails = [s.strip("\n") for s in emails_fh.readlines()]

for i, email in enumerate(emails):
	# get the persona
	if setattrs.names:
		with open(setattrs.names, "r") as names_fh:
			names = [s.strip("\n") for s in names_fh.readlines()]
		name = names[i]
	else:
		name = email.split("@")[0]

	file_name = find_certificate(name, Path(setattrs.certificates))


	# Create the root message and fill in the from, to, and subject headers
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = ' '.join(setattrs.subject)
	msgRoot['From'] = setattrs.sender
	msgRoot['To'] = email
	msgRoot.preamble = 'This is a multi-part message in MIME format.'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	# greet only if the client does not support images
	greeting = ' '.join(setattrs.subject)
	msgText = MIMEText(greeting)
	msgAlternative.attach(msgText)

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)

	img = open(file_name, "rb")
	msgImage = MIMEImage(img.read())
	img.close()

	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	import smtplib
	smtp = smtplib.SMTP("smtp.gmail.com", 587)
	smtp.starttls()
	smtp.login(setattrs.sender, pssw)
	smtp.sendmail(setattrs.sender, email, msgRoot.as_string())
	smtp.quit()