import email
import logging
import os
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from imaplib import IMAP4_SSL

## Used to download emails and parse the attachments from them
class EmailGetter:

    def __init__(self, hostname, username, password, download_path='./', max_workers=8):
        self.client = IMAP4_SSL(hostname)
        self._login(username, password)
        self.client.select("inbox")
        self.download_path = download_path
        self.hostname = hostname
        self.username = username
        self.password = password
        self.threads = max_workers
        if not os.path.exists(download_path):  # create download path if it does not exist
            os.makedirs(download_path)

    ## Log in to the email client using the provided credentials
    # @param username The username
    # @param password The password
    def _login(self, username, password):
        self.client.login(username, password)

    ## Get a list of emails since a given date
    # @param date The datetime.date object representing the date to look back to
    def get_email_list_since_date(self, date):
        status, email_list = self.client.search(None, '(SINCE "' + date.strftime("%d-%b-%Y") + '")')
        return [int(m) for m in email_list[0].split()]

    ## Download all attachments in emails since a given date
    # @param date The datetime.date object representing the date to look back to
    def download_all_attachments_since_date(self, date):
        messages = self.get_email_list_since_date(date)
        if len(messages) > 0:
            logging.info("Need to download messages: " + str(messages))
        else:
            logging.warning("No New Emails Found")

        pool = ThreadPoolExecutor(max_workers=self.threads)

        for msg_number in messages:
            pool.submit(self.threaded_download, msg_number)

        pool.shutdown(wait=True)  # join

    ## A function to download the attachment from a given email in a thread safe way
    # A single imaplib.IMAP4_SSL is NOT thread safe
    # @param message_number the number of the message to download the attachment from
    def threaded_download(self, message_number):
        try:
            logging.info("Starting thread for message " + str(message_number))
            client1 = EmailGetter(self.hostname, self.username, self.password)

            logging.info("Getting message " + str(message_number))
            ret, msg = client1.client.fetch(str(message_number), "(RFC822)")
            EmailGetter.download_attachment_from_email(email.message_from_bytes(msg[0][1]),
                                                       download_path=self.download_path)
        except Exception as e:
            print(str(e))
            logging.error(str(e))
            traceback.print_exc()

    ## Method to parse out the encoded attachment from an email attachment
    # @param message The email message object to parse the attachment from
    # @param download_path The path to download the file to on the disk, ./ by default
    @staticmethod
    def download_attachment_from_email(message, download_path='./'):
        for part in message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            att_path = os.path.join(download_path, filename)

            fp = open(att_path, 'wb')
            logging.info("Writing to " + att_path)
            fp.write(part.get_payload(decode=True))
            fp.close()

## Different approaches for downloading the emails

# ######## THREAD POOL ##########
# pool = ThreadPoolExecutor(max_workers=8)
#
# for msg_number in messages:
#     pool.submit(threaded_download, msg_number)
#

# ######## THREADS ##########
# threads = []
#
# for msg_number in messages:
#     t = Thread(target=threaded_download, args=(msg_number,))
#     threads.append(t)  # way less time :)
#     t.start()
#
# for t in threads:
#     t.join(timeout=0)
#
# ######## SYNC ##########
# for msg_number in messages:
#     non_threaded_download(msg_number) # 378 ish seconds for 149 emails
