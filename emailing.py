import imghdr
import os
import smtplib
from email.message import EmailMessage

SENDER = "profesor.rosendo@gmail.com"
RECEIVER = SENDER
PASSWORD = os.getenv("PASSWORD")


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Nuevo cliente en la tienda"
    email_message.set_content("Acaba de entrar un nuevo cliente")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image",
                                 subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com")
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email("images/send/20231023-12.40.11.png")
