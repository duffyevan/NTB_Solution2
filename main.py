import email
from datetime import date
from threading import Thread

from Email import EmailGetter


def threaded_download(message_number):
    client1 = EmailGetter("imap.mail.hostpoint.ch", "datain@wp-feldmessung.ch", "vJn4CZ3j")

    ret, msg = client1.client.fetch(str(message_number), "(RFC822)")
    client1.download_attachment_from_email(email.message_from_bytes(msg[0][1]))


def non_threaded_download(message_number):
    ret, msg = client.client.fetch(str(message_number), "(RFC822)")
    client.download_attachment_from_email(email.message_from_bytes(msg[0][1]))


client = EmailGetter("imap.mail.hostpoint.ch", "datain@wp-feldmessung.ch", "vJn4CZ3j")
today = date.today()
messages = client.get_email_list_since_date(date(2016, 5, 5))

print(messages)

threads = []

for msg_number in messages:
    t = Thread(target=threaded_download, args=(msg_number,))
    threads.append(t)  # way less time :)
    t.start()

for t in threads:
    t.join(timeout=0)
#
# for msg_number in messages:
#     non_threaded_download(msg_number) # 378 ish seconds for 149 emails
