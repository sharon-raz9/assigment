import requests
import multiprocessing

import attacker

LOGIN_WORDS = ['password', 'login', 'authentication', 'fname']
URL_BRUTE_FORCE_NAMES = 'url_brute_force_names.txt'


class UrlBruteForce:
    def __init__(self, url):
        self.url = url

    def create_url(self, extension):
        full_url = f"{self.url}{extension}"
        return full_url

    # get more url options from robots.txt
    def get_extensions_from_robots(self):
        res = requests.get(f"{self.url}/robots.txt")
        robots_list = res.text
        robots_list = robots_list.replace('Disallow: ', '')
        robots_list = robots_list.replace('Allow: ', '')
        robots_list = robots_list.splitlines()
        robots_list = [url for url in robots_list if url.startswith('/')]
        return robots_list

    def create_url_extension_list(self, extension_file_path):
        robots_extension_list = self.get_extensions_from_robots()
        # get more extensions from file
        with open(extension_file_path, 'r') as file:
            extension = file.read()
            extension_list = extension.splitlines()
            print(extension_list)
        return extension_list + robots_extension_list

    @staticmethod
    def check_if_login_page(page_text):
        w = [word for word in LOGIN_WORDS if word in page_text]
        if len(w) > 0:
            return True
        return False

    def scan_for_login_pages(self, extension_list):
        for extension in extension_list:
            url = self.create_url(extension)
            print(f'the current url is : {url}')
            try:
                res = requests.get(url)
                print(res.status_code)
                if res.status_code == 200:
                    result = UrlBruteForce.check_if_login_page(res.text)
                    if result:
                        print(f"{url} is a login page")
                        p = multiprocessing.Process(
                            target=attacker.Attacker(url).attack)
                        p.start()
            except requests.ConnectionError:
                pass

    def run(self):
        extension_list = self.create_url_extension_list(URL_BRUTE_FORCE_NAMES)
        self.scan_for_login_pages(extension_list)
