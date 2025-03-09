# Mail Sender
> Python dilinde, kişisel e-posta gönderimini otomatikleştiren bir konsol uygulaması.

## Açıklama
Sunduğu özellikler:
- Kişiselleştirilmiş mail içeriği
- Kişiselleştirilmiş mail ekleri 
- HTML / plain mail gönderebilme
- [Generate Certificate](https://github.com/seymenkonuk/generate_certificate) ile entegre olarak, sertifikaları ilgili kişilere hızlı bir şekilde mail olarak gönderebilme

## İçindekiler
<ol>
	<li>
		<a href="#başlangıç">Başlangıç</a>
		<ul>
			<li><a href="#bağımlılıklar">Bağımlılıklar</a></li>
			<li><a href="#kurulum">Kurulum</a></li>
			<li><a href="#yapılandırma">Yapılandırma</a></li>
			<li><a href="#çalıştırma">Çalıştırma</a></li>
		</ul>
	</li>
	<li><a href="#dizin-yapısı">Dizin Yapısı</a></li>
	<li><a href="#lisans">Lisans</a></li>
	<li><a href="#Iletişim">İletişim</a></li>
</ol>

## Başlangıç
### Bağımlılıklar
Proje aşağıdaki işletim sistemlerinde test edilmiştir:
- **Windows 10**
- **Windows 11**
- **Debian**

Projenin düzgün çalışabilmesi için aşağıdaki yazılımların sisteminizde kurulu olması gerekir:
- **Python Yorumlayıcısı 3.9**
- **pip**
- **Docker** (docker ortamında çalıştıracaksanız)

<p align="right">(<a href="#mail-sender">back to top</a>)</p>

---

### Kurulum
1. Bu repository'yi kendi bilgisayarınıza klonlayın:
	```bash
	git clone https://github.com/seymenkonuk/mail_sender.git
	```

2. Projeye gidin:
	```bash
	cd mail_sender
	```

<p align="right">(<a href="#mail-sender">back to top</a>)</p>

---

### Yapılandırma
1. Mailde yazacak yazı için bir şablon oluşturmak için `temp_messages/` dizini altına **"<şablon_ismi>"** adında bir dizin oluşturun. 
2. Bu dizinin altına **message.conf** ve **message.txt** adında iki dosya oluşturun.
3. **message.txt** dosyasının içine mesaj olarak yazmasını istediğiniz metni yazınız.
	```
	Merhaba İsim Soyisim,

	"EXAMPLE EVENT" etkinliğimize katılımınız için teşekkür ederiz! Aşağıda, bu etkinliğe gösterdiğiniz ilgi ve katkı için size özel olarak hazırlanmış katılım sertifikanızı bulabilirsiniz.

	Gelecek etkinliklerimizde de sizi aramızda görmekten mutluluk duyarız!
	<hr>
	Başarılarınızın devamını dileriz.
	Saygılarımızla,
	EXAMPLE COMMUNITY
	```
4. **message.txt** dosyasında 2 farklı değişken ekleyebilirsiniz:
	- **Mesaj Sabitleri**: her etkinlikte değişen bilgiler için kullanabilirsiniz.
		```
		Merhaba İsim Soyisim,

		"{{#EVENT_NAME#}}" etkinliğimize katılımınız için teşekkür ederiz! Aşağıda, bu etkinliğe gösterdiğiniz ilgi ve katkı için size özel olarak hazırlanmış katılım sertifikanızı bulabilirsiniz.

		Gelecek etkinliklerimizde de sizi aramızda görmekten mutluluk duyarız!
		<hr>
		Başarılarınızın devamını dileriz.
		Saygılarımızla,
		{{#EVENT_ORGANIZER#}}
		```
	- **Kişi Değişkenleri**: kişiye göre değişen veriler için kullanabilirsiniz.
		```
		Merhaba {{$NAME$}},

		"{{#EVENT_NAME#}}" etkinliğimize katılımınız için teşekkür ederiz! Aşağıda, bu etkinliğe gösterdiğiniz ilgi ve katkı için size özel olarak hazırlanmış katılım sertifikanızı bulabilirsiniz.

		Gelecek etkinliklerimizde de sizi aramızda görmekten mutluluk duyarız!
		<hr>
		Başarılarınızın devamını dileriz.
		Saygılarımızla,
		{{#EVENT_ORGANIZER#}}
		```
5. Mesaj sabitlerini, mail türünü ve mail konusunu **message.conf** dosyasına tanımlayınız.
	```
	[General]
	type=html
	subject=Certificate

	[Constant]
	EVENT_ORGANIZER=Example Community
	EVENT_NAME=Example Event
	EVENT_DATE=01.01.2025
	```
6. Kişi değişkenlerini **settings/mailsend.tsv** dosyasına tanımlayınız.
	```
	EMAIL	NAME	ATTACHMENTS
	example	example	example
	```
7. `ATTACHMENTS` boş bırakılırsa ek yoktur, bir dosya ise ek o dosyadır, bir dizin ise ek o dizinin içindeki tüm dosyalardır.
8. `settings/settings.conf` dosyasına kullanacağınız hesap bilgilerini, mesaj şablonunu, gönderilen mesajların hangi klasörde görüntüleyebileceğiniz ve herkese ortak olarak gönderilecek ekleri tanımlayınız.
	```
	[General]
	account_settings=account.conf
	template_message=example1

	save_to_folder=true
	folder_name=Example

	shared_attachments=shared
	```
9. `settings/account.conf` dosyasına mail'i gönderecek hesabın bilgilerini giriniz.
	```
	[General]
	email=example@recepseymenkonuk.com
	password=Example Password

	display_name=Example Name

	smtp_host=smtp.recepseymenkonuk.com
	smtp_port=587

	imap_host=imap.recepseymenkonuk.com
	imap_port=993
	```
10. Mailde gönderilecek bütün ekleri `attachments/` dizinine yerleştiriniz.

<p align="right">(<a href="#mail-sender">back to top</a>)</p>

---

### Çalıştırma

Uygulama **Docker** üzerinden kolayca çalıştırılabilir.

- **Docker image almak için**:

	```bash
	make build
	```

- **Projeyi çalıştırmak için**:

	```bash
	make run
	```

- **Mailleri göndermeden test etmek için**:

	```bash
	make test
	```

<p align="right">(<a href="#mail-sender">back to top</a>)</p>

---

## Dizin Yapısı
```
├── mail_sender/
│   ├── attachments/			#Mail ile gönderilecek ek dosyalar
│   │   └── shared/			#Mail ile herkese ortak olarak gönderilecek ek dosyalar
│   ├── settings/			#ayar dosyaları
│   ├── temp_message/			#mail içeriği şablonları
│   └── src/				#projenin kaynak kodları
```

<p align="right">(<a href="#mail-sender">back to top</a>)</p>

---

## Lisans
Bu proje [MIT Lisansı](https://github.com/seymenkonuk/mail_sender/blob/main/LICENSE) ile lisanslanmıştır.

<p align="right">(<a href="#mail-sender">back to top</a>)</p>

---

## Iletişim
Proje ile ilgili sorularınız veya önerileriniz için bana ulaşabilirsiniz:

GitHub: https://github.com/seymenkonuk

LinkedIn: https://www.linkedin.com/in/recep-seymen-konuk/

Proje Bağlantısı: [https://github.com/seymenkonuk/mail_sender](https://github.com/seymenkonuk/mail_sender)

<p align="right">(<a href="#mail-sender">back to top</a>)</p>

---
