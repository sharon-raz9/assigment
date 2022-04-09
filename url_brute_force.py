import requests

login_words = ['password', 'username', 'login']


class UrlBruteForce:
    def __init__(self, url):
        self.url = url

    def create_url(self, extension):
        full_url = f"https://{self.url}/{extension}"
        return full_url

    @staticmethod
    def create_url_extension_list(extension_file_path):
        with open(extension_file_path, 'r') as file:
            extension = file.read()
            extension_list = extension.splitlines()
            print(extension_list)
        return extension_list

    def check_if_login_page(self, page_text):
        w = [word for word in login_words if word in page_text]
        if len(w) > 0:
            return True
        return False

    def scan_for_login_pages(self, extension_list):
        for extension in extension_list:
            url = self.create_url(extension)
            try:
                res = requests.get(url)
                print(res.status_code)
                result = self.check_if_login_page(res.text)
                if result:
                    print(f"{url} is a login page")
                    # send to attacker
                print("=============================================================================")
                break
            except requests.ConnectionError:
                pass

    def run(self):
        extension_list = self.create_url_extension_list('brute_force_url_names.txt')
        self.scan_for_login_pages(extension_list)
