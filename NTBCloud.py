import logging
import posixpath

import webdav.client as wc


## Used to filter exceptions caused by this library
class NTBCloudException(Exception):
    ## Constructor
    # @param info Some information about the error
    def __init__(self, info):
        self.info = info

    ## Implementation of to string
    # @returns The info as a string
    def __str__(self):
        return self.info


## Client For Connecting To NTB's Cloud Via WebDav
class NTBWebdav:

    ## Constructor
    # @param hostname The hostname for NTB's cloud (EX: https://cloud.ntb.ch/)
    # @param username The username for someone who has access to the shared folder
    # @param password The password for that user
    def __init__(self, hostname, username, password):
        login_options = {
            'webdav_hostname': hostname,
            'webdav_login': username,
            'webdav_password': password,
            'webdav_root': '/remote.php/webdav/'
        }
        self.backup_location = "/09_SHARED_FOLDER_EXTERN/Messdaten_Feldmessung"
        self.client = wc.Client(login_options)
        logging.info("Logged Into NTB Webdav")

    ## Backs up a single file to the correct folder on NTB's Cloud
    # @param file_path The path to the file on the disk that should be backed up
    def backup_file(self, file_path, destination_path=''):
        logging.info("Backing up " + file_path)
        backup_file_name = posixpath.join(
            self.backup_location,
            posixpath.join(destination_path, posixpath.basename(file_path))
        )
        try:
            self.makeSurePathExists(destination_path)
            self.client.upload_sync(local_path=file_path, remote_path=backup_file_name)
        except wc.WebDavException as e:
            raise NTBCloudException(str(e))

    def makeSurePathExists(self, path):
        curpath = self.backup_location
        for folder in path.split('/'):
            curpath = posixpath.join(curpath, folder)
            self.client.mkdir(curpath)

    @staticmethod
    def getPathFromFileName(filename):
        parts = filename.strip('.xls').split('_')
        number = parts[0]
        date = parts[1]
        year = date[:4]
        month = date[4:6]
        return "%s/%s/%s" % (number, year, month)

