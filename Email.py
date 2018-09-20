import os


def download_attachment_from_email(message, download_path='./'):
    for part in message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        att_path = os.path.join(download_path, filename)

        if not os.path.isfile(att_path):
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()


def get_email_list_from_date(client, date):
    status, email_list = client.search(None, '(SINCE "' + date.strftime("%d-%b-%Y") + '")')
    return email_list
