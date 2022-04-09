import requests
from scanner import Scanner


class UrlBruteForceScanner(Scanner):
    def __init__(self, domain, file_path):
        super().__init__(domain)
        self.file_path = file_path

    def create_url(self, url):
        url = f"https://{self.domain}/{url}"
        return url

    def scanner(self):
        urls_list = Scanner.create_names_list(self.file_path)
        self.url_validator(urls_list)
        print(f'verified_urls {self.verified_urls}')
