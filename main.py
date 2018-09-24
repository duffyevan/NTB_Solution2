import multiprocessing
import sys
from datetime import date

from Email import EmailGetter

login_info = open("email.csv", 'r').readline().split(',')

download_path = sys.argv[1] if len(sys.argv) > 1 else './downloads/'

client = EmailGetter(login_info[0], login_info[1], login_info[2],
                     max_workers=multiprocessing.cpu_count(), download_path=download_path)

client.download_all_attachments_since_date(date(2016, 5, 5))
