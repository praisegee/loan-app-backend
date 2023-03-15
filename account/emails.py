import threading

from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailThread(threading.Thread):

    def __init__(self, subject, plain_message, html_message, from_email, receiver):
        threading.Thread.__init__(self)
        self.subject = subject
        self.plain_message = plain_message,
        self.from_email = from_email
        self.receiver = receiver
        self.html_message = html_message

    def run(self):
        mail.send_mail(self.subject, str(self.plain_message), self.from_email, self.receiver, html_message=self.html_message)

class Email:
    
    def __init__(self, subject:str="Loan App", receiver:str="", plain_message:str="", template:str="", data={}) -> None:
        self.template = template
        self.plain_message = plain_message
        self.from_email = 'loanapp@company.com'
        self.receiver = receiver if isinstance(receiver, list) else [receiver]
        self.subject = subject
        self.data = data
    
    def send(self):
        try:
            html_message = render_to_string(f'{self.template}', self.data)
            EmailThread(self.subject, self.plain_message, html_message, self.from_email, self.receiver).start()
        except:
            pass
