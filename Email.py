import os
from imaplib import IMAP4_SSL


class EmailGetter:

    def __init__(self, hostname, username, password):
        self.client = IMAP4_SSL(hostname)
        self._login(username, password)
        self.client.select("inbox")

    def _login(self, username, password):
        self.client.login(username, password)

    def get_email_list_since_date(self, date):
        status, email_list = self.client.search(None, '(SINCE "' + date.strftime("%d-%b-%Y") + '")')
        return [int(m) for m in email_list[0].split()]



    @staticmethod
    def download_attachment_from_email(message, download_path='./'):
        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            att_path = os.path.join(download_path, filename)

            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                print ("Writing to " + att_path)
                fp.write(part.get_payload(decode=True))
                fp.close()

