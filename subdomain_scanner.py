import requests
import multiprocessing

import url_brute_force


class SubDomainScanner:
    def __init__(self, domain):
        self.domain = domain

    def create_url(self, sub_domain):
        url = f"https://{sub_domain}.{self.domain}"
        return url

    @staticmethod
    def create_sub_domain_list(names_file_path):
        with open(names_file_path, 'r') as file:
            sub_domain_names = file.read()
            sub_domain_names = sub_domain_names.splitlines()
            print(sub_domain_names)
        return sub_domain_names

    # def check_if_login_page(self, page_text):
    #     w = [word for word in login_words if word in page_text]
    #     if len(w) > 0:
    #         return True
    #     return False

    def sub_domains_validator(self, sub_domains_names_list):
        proc = list()
        for sub_domain_name in sub_domains_names_list:
            url = self.create_url(sub_domain_name)
            try:
                res = requests.get(url)
                p = multiprocessing.Process(
                    target=url_brute_force.UrlBruteForce(url).run())
                p.start()
                proc.append(p)
                print("=============================================================================")
            except requests.ConnectionError:
                pass
        for p in proc:
            p.join()

    def scan(self):
        sub_domain_list = self.create_sub_domain_list('sub_domains_names.txt')
        self.sub_domains_validator(sub_domain_list)
