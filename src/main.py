import sys

from helper.mail import MailSender
from helper.file import read_tsv_file

def main():
	mail = MailSender()
	message, settings = mail.read_template_message()
	
	for receiver in read_tsv_file("settings/mailsend.tsv"):
		# Kişiye Özel Mesajı Hazırla
		content = message
		for key, value in receiver.items():
			content = content.replace("{{$"+key+"$}}", value)
		# Fonksiyonu Seç
		if sys.argv[1] == "test":
			func = mail.test
		elif settings["type"] == "html":
			func = mail.sendHTML
		else:
			func = mail.send_plain
		# Fonksiyonu Çalıştır
		func(receiver["EMAIL"], settings["subject"], content, receiver["ATTACHMENTS"])

if __name__ == "__main__":
	main()
