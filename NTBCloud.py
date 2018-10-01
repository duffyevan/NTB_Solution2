import os

import webdav.client as wc


class NTBCloudException(Exception):
    def __init__(self, info):
        self.info = info

    def __str__(self):
        return self.info


class NTBWebdav:
    def __init__(self, hostname, username, password):
        login_options = {
            'webdav_hostname': hostname,
            'webdav_login': username,
            'webdav_password': password
        }
        self.backup_location = "/remote.php/webdav/09_SHARED_FOLDER_EXTERN/"
        self.client = wc.Client(login_options)

    def backup_file(self, file_path):
        backup_file_name = os.path.join(self.backup_location, os.path.basename(file_path))
        try:
            self.client.upload_sync(local_path=file_path, remote_path=backup_file_name)
        except wc.WebDavException as e:
            raise NTBCloudException(str(e))
