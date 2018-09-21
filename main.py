import multiprocessing
from datetime import date

from Email import EmailGetter

client = EmailGetter("imap.mail.hostpoint.ch", "datain@wp-feldmessung.ch", "vJn4CZ3j",
                     max_workers=multiprocessing.cpu_count(), download_path='./downloads/')

client.download_all_attachments_since_date(date(2016, 5, 5))
