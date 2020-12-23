from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

def find_his_certificate(name, path):
	name_parts = name.split(".-_")
	for file in os.listdir(path):
		for part in name_parts:
			if part not in file:
				continue 


# Define these once; use them twice!
strFrom = 'ekaterina.dvoretckaia@gmail.com'
print("Enter sender's mail password:")
pssw = input().strip("\n")
with open("emails.txt", "r") as emails_fh:
	emails = [s.strip("\n") for s in emails_fh.readlines()]

for e in emails:
	strTo = e
	# get the persona
	name = strTo.split("@")[0]

	file_name = find_his_certificate(name, "pdfout")


	# Create the root message and fill in the from, to, and subject headers
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Happy New Year 2021!'
	msgRoot['From'] = strFrom
	msgRoot['To'] = strTo
	msgRoot.preamble = 'This is a multi-part message in MIME format.'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	# greet only if the client does not support images
	greeting = """
	I wish you Merry Christmas and Happy New Year 2021!
	Let your hopes and dreams become true in the coming year!
	All the best,
	Ekaterina Dvoretckaia
	Ex2002B040824
	"""
	msgText = MIMEText(greeting)
	msgAlternative.attach(msgText)

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)

	img = open("pdfout/certificate_Adelma_Di_Biasio.jpg", "rb")
	msgImage = MIMEImage(img.read())
	img.close()

	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	import smtplib
	smtp = smtplib.SMTP("smtp.gmail.com", 587)
	smtp.starttls()
	smtp.login(strFrom, pssw)
	smtp.sendmail(strFrom, strTo, msgRoot.as_string())
	smtp.quit()