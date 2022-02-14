import smtplib, ssl
import os
from email.message import EmailMessage
from secrects import email_user, email_pass


smtp_server = 'smtp server address'
smtp_port = 587

context = ssl.create_default_context()



def email(path,attachment):
	file = os.path.join(os.path.expanduser(path), attachment)
	msg = EmailMessage()
	msg['From'] = 'from address'
	msg['Subject'] = 'Switch Backup Logs'
	msg['To'] = 'to address,add another address'
	msg.set_content('An error occurred with the daily switch backup. Please review attched logfile \n')
	msg.add_attachment(open(file, "r").read())

	s = smtplib.SMTP(smtp_server, smtp_port)
	s.login(email_user, email_pass)
	s.send_message(msg)

	print("email sent out successfully")

if __name__ == "__email__":
    email()
