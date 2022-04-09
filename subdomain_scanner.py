import requests
from scanner import Scanner


class SubDomainScanner(Scanner):
    def __init__(self, domain, file_path):
        super().__init__(domain)
        self.file_path = file_path

    def create_url(self, sub_domain):
        url = f"https://{sub_domain}.{self.domain}"
        return url

    def scanner(self):
        urls_list = Scanner.create_names_list(self.file_path)
        self.url_validator(urls_list)
        print(f'verified_urls {self.verified_urls}')
