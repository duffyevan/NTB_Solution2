import multiprocessing
from datetime import date

from Email import EmailGetter

login_info = open("email.csv", 'r').readline().split(',')

client = EmailGetter(login_info[0], login_info[1], login_info[2],
                     max_workers=multiprocessing.cpu_count(), download_path='./downloads/')

client.download_all_attachments_since_date(date(2016, 5, 5))
