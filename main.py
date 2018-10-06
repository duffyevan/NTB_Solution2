import logging
import multiprocessing
import os
import sys
from datetime import date, timedelta
from shutil import copyfile

from ConsistencyChecker import ConsistencyChecker
from Email import EmailGetter
from NTBCloud import NTBWebdav, NTBCloudException


def expected_login_format():
    print("Expected Format Of login.csv: ")
    print("\tSMTP-Hostname,emailaddress,emailpassword")
    print("\twebdavaddress,ntbusername,ntbpassword")


lookback_days = 7  # The number of days to download email before today

# Set up the log file and correct formatting
logging.basicConfig(filename="log.txt", level=logging.INFO, format='%(asctime)s: %(levelname)s : %(message)s')
logging.info("Starting...")

# Attempt to read email login info from login.csv
login_info = []
try:
    login_file = open("login.csv", 'r')
    login_info = login_file.readline().strip().split(',')
    ntb_login_info = login_file.readline().strip().split(',')
except IOError:
    print("Failed To Read login.csv!")
    logging.fatal("Failed To Read login.csv, this file must exist and contain host, user, and password for the email "
                  "client.")
    expected_login_format()
    sys.exit(-1)  # close the program with an error code

# if we havent specified the destination path in the command, exit with code and print usage
# ex: python3 main.py /home/wpfeldme/www/auto.wp-feldmessung.ch/file_content/new
if len(sys.argv) < 2:
    print("Usage: python3 main.py <download destination path>")
    exit(-1)

# download_path = sys.argv[1] if len(sys.argv) > 1 else './downloads/'
download_path = './downloads/'  # temporary download destination
destination_path = sys.argv[1]  # set the destination path to the path specified in the command

# makes sure the destination path exists, if not, create it
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

logging.debug("Download to " + download_path)

# log into the email client with the email getter class (Set the max workers (threads) to half the CPU count)
client = None
try:
    client = EmailGetter(login_info[0], login_info[1], login_info[2],
                         max_workers=multiprocessing.cpu_count() / 2, download_path=download_path)
except IndexError:
    expected_login_format()
    exit(-1)
logging.info("Logged into the email server")

# get the date that we should look back to for downloading since
download_since_date = date.today() - timedelta(lookback_days)  # download since today minus 31 days

# list the dir
old_files = os.listdir(download_path)

# download the files
client.download_all_attachments_since_date(download_since_date)

# list dir again
combined_files = os.listdir(download_path)

# difference the lists to get the new files
new_files = list(set(combined_files) - set(old_files))

# if there are any new files, print the file names for debugging purposes
if len(new_files) > 0:
    print("Got New Files: " + str(new_files))
    logging.info("Got New Files: " + str(new_files))

ntb_client = None
try:
    ntb_client = NTBWebdav(ntb_login_info[0], ntb_login_info[1], ntb_login_info[2])
except IndexError:
    expected_login_format()
    exit(-1)

# for each new file copy it from the temp download folder to the final destination folder
for file in new_files:
    src = os.path.join(download_path, file)
    dest = os.path.join(destination_path, file)
    copyfile(src, dest)

    try:
        ntb_client.backup_file(dest)  # make a backup to NTB's cloud
    except NTBCloudException as ex:
        logging.error("Failed to backup " + file + " to NTB's Cloud!")
        logging.error("Webdav Error Info: " + str(ex))
        print("Failed to backup " + file + " to NTB's Cloud!")

checker = ConsistencyChecker()
checker.check_consistency(download_path)

logging.info("Done. Exiting")
