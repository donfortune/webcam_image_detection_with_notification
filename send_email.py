
import smtplib
import ssl
import imghdr  #gives metadata about images
from email.message import EmailMessage
def send_email(image_path):
    host = "smtp.gmail.com"
    port = 465
    username = 'donfortunet.df@gmail.com'
    password = 'xxxxxxxxxxxxxxxxxx'
    receiver_email = 'osowoayiobi@gmail.com'
    message = EmailMessage(). #from the imported module
    message['Subject'] = 'New Image Found'
    message.set_content('New image')

    with open(image_path, 'rb') as file:
        content = file.read()
        message.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as file:
        file.login(username, password)
        file.sendmail(username, receiver_email, message.as_string())
        file.quit()


if __name__ == "__main__":
    send_email(image_path='images/19.jpeg')
