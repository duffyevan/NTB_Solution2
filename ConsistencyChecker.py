import os
from datetime import date, timedelta, datetime

from EmailSender import EMailSender, EMail


class ConsistencyChecker:
    def __init__(self):
        login_info = open('login.csv').readlines()[2].strip().split(',')
        self.email_login = login_info
        self.email_client = EMailSender(login_info[0], login_info[1])
        self.email_client.login(login_info[2], login_info[3])

    def check_consistency(self, directory):
        yesterdays_list = self.get_plcs_for_day(date.today() - timedelta(days=1), directory)
        two_days_ago_list = self.get_plcs_for_day(date.today() - timedelta(days=2), directory)
        missing_plcs = set()
        for plc in two_days_ago_list:
            if plc not in yesterdays_list:
                missing_plcs.add(plc)
        if len(missing_plcs) > 0:
            print("PLC MISSING!!!")
            print("Missing PLCS: " + str(missing_plcs))
            for plc in missing_plcs:
                email = EMail(self.email_login[2], self.email_login[2])  # TODO set destination email to a target
                email.set_body("SPS Number " + str(plc) + " Did Not Send An Email Today!!")
                email.set_subject("SPS #" + str(plc) + " Missing")
                self.email_client.send_message(email)

    def get_plcs_for_day(self, day, directory):
        plc_numbers = set()
        for filename in os.listdir(directory):
            data = self.__name_to_plc_and_date(filename)
            if data[1].__eq__(day):
                plc_numbers.add(data[0])
        return plc_numbers

    @staticmethod
    def __name_to_plc_and_date(filename):
        if '.xls' not in filename:
            print("Data Not Found For " + filename)
            return None
        parts = filename.replace('.xls', '').split('_')
        number = int(parts[0].replace('F', ''))
        d = datetime.strptime(parts[1], "%Y%m%d").date()
        return number, d


if __name__ == '__main__':
    c = ConsistencyChecker()
    c.check_consistency('./downloads')
