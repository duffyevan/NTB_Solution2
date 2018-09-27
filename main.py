import logging
import multiprocessing
import os
import sys
from shutil import copyfile
from datetime import date, timedelta

from Email import EmailGetter

lookback_days = 7

logging.basicConfig(filename="log.txt", level=logging.INFO, format='%(asctime)s: %(levelname)s : %(message)s')
logging.info("Starting...")
login_info = []
try:
    login_info = open("email.csv", 'r').readline().strip().split(',')
except:
    print("Failed To Read email.csv!")
    logging.fatal("Failed To Read email.csv, this file must exist and contain host, user, and password for the email "
                  "client.")
    sys.exit(-1)


if len(sys.argv) < 2:
    print("Usage: python3 main.py <download destination path>")
    exit(-1)
# download_path = sys.argv[1] if len(sys.argv) > 1 else './downloads/'
download_path = './downloads/'
destination_path = sys.argv[1]
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

logging.debug("Download to " + download_path)

client = EmailGetter(login_info[0], login_info[1], login_info[2],
                     max_workers=multiprocessing.cpu_count() / 2, download_path=download_path)
logging.info("Logged into the email server")

download_since_date = date.today() - timedelta(lookback_days)  # download since today minus 31 days

old_files = os.listdir(download_path)

client.download_all_attachments_since_date(download_since_date)

combined_files = os.listdir(download_path)

new_files = list(set(combined_files) - set(old_files))
if len(new_files) > 0:
    print("Got New Files: " + str(new_files))
    logging.info("Got New Files: " + str(new_files))

for file in new_files:
    src = os.path.join(download_path, file)
    dest = os.path.join(destination_path, file)
    copyfile(src, dest)

logging.info("Done. Exiting")
