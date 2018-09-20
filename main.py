import imaplib
import email
import os
from datetime import date

from Email import download_attachment_from_email, get_email_list_from_date

client = imaplib.IMAP4_SSL("imap.mail.hostpoint.ch")
client.login("datain@wp-feldmessung.ch", "vJn4CZ3j")
client.select("inbox")

ret, data = client.fetch("150", "(RFC822)")

m = email.message_from_bytes(data[0][1])

today = date.today()
print("Email List: " + str(get_email_list_from_date(client, date.today())))


# for msg in messages:
#     download_attachment_from_email(msg)


