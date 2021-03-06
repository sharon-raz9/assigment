import requests
import multiprocessing

import url_brute_force

# Other ways to discover subdomains are: by dns records, ssl and more.
# I did not have time to implement it or use other people's existing code
# but I researched on it and learned the subject

COMMON_PORTS = [443, 80, 9999, 9000, 3000]
SUB_DOMAINS_NAMES_FILE = 'sub_domains_names.txt'


class SubDomainScanner:
    def __init__(self, domain):
        self.domain = domain

    def create_url(self, sub_domain, https=False, port=None):
        if port:
            port = f':{port}'
        if https:
            return f"https://{sub_domain}.{self.domain}{port if port else ''}"
        else:
            return f"http://{sub_domain}.{self.domain}{port if port else ''}"

    @staticmethod
    def create_sub_domain_list(names_file_path):
        with open(names_file_path, 'r') as file:
            sub_domain_names = file.read()
            sub_domain_names = sub_domain_names.splitlines()
            print(f'sub domain names is: {sub_domain_names}')
        return sub_domain_names

    def check_url_and_send_to_brute_force(self, sub_domain_name, port, is_https):
        p = None
        url = self.create_url(sub_domain_name, https=is_https, port=port)
        print(f'the current sub domain url is : {url}')
        res = requests.get(url)
        print(res)
        if res.status_code == 200:
            p = multiprocessing.Process(
                target=url_brute_force.UrlBruteForce(url).run)
            p.start()

    def sub_domains_validator(self, sub_domains_names_list):
        for sub_domain_name in sub_domains_names_list:
            for port in COMMON_PORTS:
                try:
                    self.check_url_and_send_to_brute_force(sub_domain_name, port, True)
                except requests.ConnectionError:
                    try:
                        self.check_url_and_send_to_brute_force(sub_domain_name, port, False)
                    except requests.ConnectionError:
                        continue

    def scan(self):
        sub_domain_list = self.create_sub_domain_list(SUB_DOMAINS_NAMES_FILE)
        self.sub_domains_validator(sub_domain_list)
