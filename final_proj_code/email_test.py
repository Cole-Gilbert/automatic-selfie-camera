import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def send_email(sender_email, sender_password, receiver_email, subject, body, image_path):
	#MIME setup
	message = MIMEMultipart()
	message['From'] = sender_email
	message['To'] = receiver_email
	message['Subject'] = subject

	#attach body of message
	message.attach(MIMEText(body, 'plain'))

	#attach image to file
	with open(image_path, 'rb') as file:
		img = MIMEImage(file.read())
		message.attach(img)

	#send email via SMTP server
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
		server.login(sender_email, sender_password)
		server.sendmail(sender_email, receiver_email, message.as_string())

def email_main():
	correct_email = False
	receiver_email = ""
	select = ""
	while correct_email == False:
		receiver_email = input("Enter the recipient's email address: ")
		select = input("Is " + receiver_email + " the correct address? (y/n)")
		if select == "y" or select == "Y":
			correct_email = True

	sender_email = "ece5725selfiecam@gmail.com"
	sender_password = "outryozkdudjoiaq"
	subject = "Automated Test"
	message = "Hey did this work??"
	image_path = "/home/pi/final_proj/test.jpg"

	#sending email
	send_email(sender_email, sender_password, receiver_email, subject, message, image_path)

email_main()
