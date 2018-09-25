import logging
import multiprocessing
import sys
from datetime import date

from Email import EmailGetter

logging.basicConfig(filename="log.txt", level=logging.INFO, format='%(asctime)s: %(levelname)s : %(message)s')
logging.info("Starting...")
try:
    login_info = open("email.csv", 'r').readline().strip().split(',')
except:
    print("Failed To Read email.csv!")
    logging.fatal("Failed To Read email.csv, this file must exist and contain host, user, and password for the email "
                  "client.")

download_path = sys.argv[1] if len(sys.argv) > 1 else './downloads/'

logging.debug("Download path set to " + download_path)

client = EmailGetter(login_info[0], login_info[1], login_info[2],
                     max_workers=multiprocessing.cpu_count() / 2, download_path=download_path)
logging.info("Logged into the email server")

client.download_all_attachments_since_date(date(2016, 5, 5))

logging.info("Done. Exiting")
