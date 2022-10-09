import email
import imaplib

from lib.config import *
from lib.secrets import *
from time import sleep



class Email_:

    def __init__(self, subject=None, to=None, from_=None, date=None, message=None):
        self.subject = subject
        self.to = to
        self.from_ = from_
        self.date = date
        self.message = message


class Price:

    def __init__(self, ticker=None, last=-1, prev_close=0, month=None, desc=None, inco=None, loc=None):

        self.ticker = ticker
        self.last = last
        self.prev_close = prev_close
        self.month = month
        self.desc = desc
        self.inco = inco
        self.loc = loc
        self.last_updated = None


class Price_Manager:

    def __init__(self):
        pass

    def update_prices(self, prices):

        # clear out the prices, so that later only updated prices are sent
        for price in prices:
            price.last = -1

        emails = None

        # find if there are any BZ prices & update them w/ data from FUSION
        for price in prices:
            if price.ticker == BZ:
                emails = self.__get_FUSION_emails()
                self.__update_BZ_prices(prices, emails)
                break


    def __get_FUSION_emails(self):
        #returns a list of emails of type Email_

        emails = []

        try:

            # try up to 5 times to connect to GMAIL service
            for i in range(5):

                print('\nAttempting to connect to GMAIL, try # ', i+1)

                # set connection
                mail = imaplib.IMAP4_SSL(GMAIL_HOST)

                # log in
                mail.login(USERNAME, APP_PASSWORD)

                # mail folder select
                mail.select(INBOX)

                # select specific emails - those from FUSION
                flag, selected_emails = mail.search(None, FROM_FUSION)

                if flag == OK:
                    print('\nSuccessfully connected to GMAIL')
                    break

                print('\nError in connecting to email server, flag: ', flag)
                sleep(3)

        except:
            print('\nSomething went wrong when trying to connect to gmail in Price_Manager class / __get_FUSION_emails function')

        # build a list of Email_s from the selected_emails
        for num in selected_emails[0].split():

            _, data = mail.fetch(num, '(RFC822)')
            _, bytes_data = data[0]
            email_ = Email_()

            # convert byte data to message
            email_message = email.message_from_bytes(bytes_data)

            email_.subject = email_message[SUBJECT]
            email_.to      = email_message[TO]
            email_.message = email_message[FROM]
            email_.date    = email_message[DATE]

            for part in email_message.walk():
                if part.get_content_type() == TEXT_PLAIN or part.get_content_type() == TEXT_HTML:
                    email_.message = part.get_payload(decode=True).decode()
                    break

            emails.append(email_)

        return emails

    # update all BZ prices (last element) in prices from data in emails
    def __update_BZ_prices(self, prices, emails):

        self.__update_USGC_BZ_prices(prices, emails)
        self.__update_EU_BZ_prices(prices, emails)


    def __get_most_recent_email(self, emails, subject):
        for email_ in reversed(emails):
            if subject in email_.subject:
                return email_


    def __update_USGC_BZ_prices(self, prices, emails):

        # find most recent email with USGC BZ pricing... with "BZ" in subject
        email_ = self.__get_most_recent_email(emails, BZ)

        # split the message into a list of words
        for i, word in enumerate(email_.message.split()):

            # breaking condition
            if word == "Regards" or word == "Information":
                break

            # if the word in the email is a month... the we have pricing data
            if word in MONTHS:
                next_word = email_.message.split()[i+1]
                next_next_word = email_.message.split()[i+2]
                next_next_next_word = email_.message.split()[i+3]

                # CASE 1: BZ price for Houston, DDP
                if next_word == DDP and next_next_word != LMR:

                    # calculate the new price
                    potential_price = next_next_word
                    p = self.__calculate_price_helper(potential_price)

                    # update prices for BZ HOU
                    for price in prices:
                        if word == price.month and next_word == price.inco and HOU == price.loc:
                            price.last = p
                            price.last_updated = email_.date

                # CASE 2: BZ prices for LMR, DDP
                if next_word == DDP and next_next_word == LMR:

                    # calculate the new price
                    potential_price = next_next_next_word
                    p = self.__calculate_price_helper(potential_price)

                    # update prices for BZ LMR
                    for price in prices:
                        if word == price.month and next_word == price.inco and next_next_word == price.loc:
                            price.last = p
                            price.last_updated = email_.date


    def __update_EU_BZ_prices(self, prices, emails):
        pass
        #TODO


    def __calculate_price_helper(self, potential_price):
        p=-1
        try:
            bid = int(potential_price.split('-')[0])
            ask = int(potential_price.split('-')[1])
            p = (bid + ask)/2.0

        except:
            p = -1

        return p
