# modules
from email import message
import imaplib
import email
from bs4 import BeautifulSoup
from modules.filterprocessingcrypto import FilterProcessingCrypto
from modules.filterprocessingstock import FilterProcessingStock
from modules.config import *
import requests


class ImapProcessing:
    username, app_password, gmail_host, mail, selected_mails, messages, dataset = '', '', '', None, None, None, []

    def __init__(self):
        username = 'imap.venru@gmail.com'
        app_password = 'nmzqoosgscyliokj'
        gmail_host = 'imap.gmail.com'
        self.username, self.app_password, self.gmail_host = username, app_password, gmail_host

    def initial_processing(self):
        username, app_password, gmail_host = self.username, self.app_password, self.gmail_host

        def auth(username, app_password, gmail_host):
            mail = imaplib.IMAP4_SSL(gmail_host)
            result, data = mail.login(username, app_password)
            return result, mail

        self.messages, self.mail = auth(username, app_password, gmail_host)
        self.mail.select("INBOX")

    def relogin_to_email_then_get_data(self, str_request_data, str_subject):
        while True:
            self.initial_processing()
            assert self.messages == 'OK', 'login failed'
            try:
                _, self.selected_mails = self.mail.search(
                    None, '(FROM "noreply@tradingview.com" UNSEEN SUBJECT "Screener Alert: {}")'.format(str_subject))
                self.processing_signal(str_request_data)
            except:
                continue
            break
        self.mail.logout()

    def processing_signal(self, condition):
        messages = self.selected_mails[0].split()
        soup = None
        for num in messages:
            _, data = self.mail.fetch(num, '(RFC822)')
            _, bytes_data = data[0]
            email_message = email.message_from_bytes(bytes_data)
            for part in email_message.walk():
                if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                    message = part.get_payload(decode=True)
                    soup = BeautifulSoup(message.decode(), "html.parser")
                    elements = soup.find_all('a', attrs={
                                             'style': 'text-decoration: none; color: #2962FF; word-break: break-word;', 'class': 'link'})
                    if (condition == "stock"):
                        elements_filter = [
                            result.text for result in elements[:-2]]
                    elif (condition == "crypto"):
                        elements_filter = [
                            result.text for result in elements[:-2] if "USDTPERP" in result.text.upper()]
                    for result in elements_filter:
                        self.dataset.append(result.split(":")[1])
                    self.dataset = list(set(self.dataset))
                    break

    def processing_message(self, dataset, title):
        message = title + "\n\n"
        if (len(dataset) == 0):
            message += "No Signal !\n"
        else:
            dataset.sort()
            for i in dataset:
                message += i + "\n"
        return message

    def send_to_telegram_crypto(self, message):
        URL = "https://api.telegram.org/{}/sendMessage".format(TELEGRAM_TOKEN)
        PARAMS = {'chat_id': '-640350956', 'text': message}
        requests.get(url=URL, params=PARAMS)

    def send_to_telegram_stock(self, message):
        URL = "https://api.telegram.org/{}/sendMessage".format(TELEGRAM_TOKEN)
        PARAMS = {'chat_id': '-619283146', 'text': message}
        requests.get(url=URL, params=PARAMS)

    # === START STOCK === #
    def stock_signal(self):
        self.relogin_to_email_then_get_data(
            "stock", "New Screener Simple Stock StevenRu")

        filtering = FilterProcessingStock()
        [dataset_signal, irisan] = filtering.process_data(self.dataset, "long")
        if (len(dataset_signal) > 0):
            title = "Potensi Saham Bursa Berikutnya (Ada {} Saham):\n[TICKER | CHANGE | VOLUME | CLOSE]".format(
                len(dataset_signal))
            messages = self.processing_message(dataset_signal, title)
            self.send_to_telegram_stock(messages)

    def stock_signal_debug(self, arr):
        dataset_signal = arr

        filtering = FilterProcessingStock()
        [dataset_signal, irisan] = filtering.process_data(
            dataset_signal, "long")
        if (len(dataset_signal) > 0):
            title = "Potensi Saham Bursa Berikutnya (Ada {} Saham):\n[TICKER | CHANGE | VOLUME | CLOSE]".format(
                len(dataset_signal))
            messages = self.processing_message(dataset_signal, title)
            self.send_to_telegram_stock(messages)

    # === END STOCK === #

    # === START CRYPTO === #
    def long_crypto_signal(self):
        self.relogin_to_email_then_get_data("crypto", "Long Future VenRu")

        filtering = FilterProcessingCrypto()
        [dataset_signal, irisan] = filtering.process_data(self.dataset, "long")
        if (len(dataset_signal) > 0):
            title = "Potensi Crpto Naik 1 Jam Mendatang [Long] (Ada {} Crypto) :\n[TICKER | CHANGE]".format(
                len(dataset_signal))
            messages = self.processing_message(dataset_signal, title)
            self.send_to_telegram_crypto(messages)

    def short_crypto_signal(self):
        self.relogin_to_email_then_get_data("crypto", "Short Future VenRu")

        filtering = FilterProcessingCrypto()
        [dataset_signal, irisan] = filtering.process_data(
            self.dataset, "short")
        if (len(dataset_signal) > 0):
            title = "Potensi Crpto Turun 1 Jam Mendatang [Short] (Ada {} Crypto) :\n[TICKER | CHANGE]".format(
                len(dataset_signal))
            messages = self.processing_message(dataset_signal, title)
            self.send_to_telegram_crypto(messages)

    def long_crypto_signal_debug(self, arr):
        dataset_signal = arr

        filtering = FilterProcessingCrypto()
        [dataset_signal, irisan] = filtering.process_data(
            dataset_signal, "long")
        if (len(dataset_signal) > 0):
            title = "Potensi Crpto Naik 1 Jam Mendatang [Long] (Ada {} Crypto) :\n[TICKER | CHANGE]".format(
                len(dataset_signal))
            messages = self.processing_message(dataset_signal, title)
            self.send_to_telegram_crypto(messages)

    def short_crypto_signal_debug(self, arr):
        dataset_signal = arr

        filtering = FilterProcessingCrypto()
        [dataset_signal, irisan] = filtering.process_data(
            dataset_signal, "short")
        if (len(dataset_signal) > 0):
            title = "Potensi Crpto Turun 1 Jam Mendatang [Short] (Ada {} Crypto) :\n[TICKER | CHANGE]".format(
                len(dataset_signal))
            messages = self.processing_message(dataset_signal, title)
            self.send_to_telegram_crypto(messages)

    # === END CRYPTO === #
