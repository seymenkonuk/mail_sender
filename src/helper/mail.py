import smtplib
import imaplib

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from pathlib import Path

from helper.file import read_conf_file, read_file


class MailSender:
	def __init__(self):
		self.__connect()

	def __connect(self):
		try:
			self.__settings = read_conf_file("settings/settings.conf")
			account_settings = read_conf_file(f"settings/{self.__settings['General']['account_settings']}")
			auth = account_settings["General"]
			
			self.__e_mail = auth["email"]
			self.__display_name = auth["display_name"]
			self.__smtp = smtplib.SMTP(auth["smtp_host"], auth["smtp_port"])
			self.__smtp.ehlo()
			self.__smtp.starttls()
			self.__smtp.login(auth["email"], auth["password"])

			self.__imap = imaplib.IMAP4_SSL(auth["imap_host"], auth["imap_port"])
			self.__imap.login(auth["email"], auth["password"])
		except:
			print("Connect Error")

	def __del__(self):
		try:
			self.__smtp.close()
			self.__imap.logout()
		except:
			pass

	def __send(self, message):
		self.__smtp.sendmail(message["From"], message["To"], message.as_string())

		if self.__settings['General']["save_to_folder"] == "true":
			self.__create_folder_if_not_exists(self.__settings['General']["folder_name"])
			self.__imap.select(self.__settings['General']["folder_name"])
			self.__imap.append(self.__settings['General']["folder_name"], '\\Seen', None, message.as_bytes())

	def __create_folder_if_not_exists(self, folder_name):
		status, folders = self.__imap.list()
		folder_exists = False

		for folder in folders:
			if folder_name in folder.decode():
				folder_exists = True
				break

		if not folder_exists:
			self.__imap.create(folder_name)

	def __create_message(self, to, subject, content, subtype):
		message = MIMEMultipart()
		message['From'] = f"{Header(self.__display_name, 'utf-8').encode()} <{self.__e_mail}>"
		message["Subject"] = subject
		message["To"] = to
		message.attach(MIMEText(content, subtype))
		return message

	def __create_message_with_attachments(self, to, subject, content, subtype, attachment_path):
		message = self.__create_message(to, subject, content, subtype)

		attachment_paths = self.__find_attachments_files(attachment_path)

		for attachment_path in attachment_paths:
			try:
				with open(attachment_path, 'rb') as attachment:
					part = MIMEBase('application', 'octet-stream')
					part.set_payload(attachment.read())
					encoders.encode_base64(part)
					part.add_header(
						'Content-Disposition',
						f'attachment; filename={attachment_path.split("/")[-1]}',
					)
					message.attach(part)
			except Exception as e:
				print(f'Attachments File Error: {e}')
				return
		
		return message
	
	def __find_attachments_files(self, attachments_path=""):
		result = []

		attachments_paths = []
		if self.__settings['General']["shared_attachments"] != "":
			attachments_paths.append("attachments/" + self.__settings['General']["shared_attachments"])
		if attachments_path != "":
			attachments_paths.append("attachments/" + attachments_path)

		for path in attachments_paths:
			p = Path(path)
			if p.is_file():
				result.append(str(p))
			elif p.is_dir():
				result.extend([str(f) for f in p.rglob("*") if f.is_file()])

		return result

	def sendHTML(self, to, subject, content, attachments_path=""):
		message = self.__create_message_with_attachments(to, subject, content, "html", attachments_path)
		self.__send(message)

	def send_plain(self, to, subject, content, attachments_path=""):
		message = self.__create_message_with_attachments(to, subject, content, "plain", attachments_path)
		self.__send(message)
	
	def test(self, to, subject, content, attachments_path=""):
		message = self.__create_message_with_attachments(to, subject, content, "plain", attachments_path)
		print("To:", to)
		print("Subject:", subject)
		print("Attachments:", attachments_path)
		# print(f"\n{message.as_string()}",end="\n")
		print("*"*30)
	
	def read_template_message(self):
		# Mesaj Template'ini Oku
		message_content = read_file(f"temp_messages/{self.__settings['General']['template_message']}/message.txt")
		message_conf = read_conf_file(f"temp_messages/{self.__settings['General']['template_message']}/message.conf")
		# Mesaj Template'teki Constant'ları Düzelt
		for key, value in message_conf["Constant"].items():
			message_content = message_content.replace("{{#"+key+"#}}", value)
		# Return
		return message_content, message_conf["General"]
