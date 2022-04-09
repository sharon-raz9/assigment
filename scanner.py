import requests

login_words = ['password', 'username', 'login']


class Scanner:
    def __init__(self, domain):
        self.domain = domain
        self.verified_urls = list()

    def create_url(self, names):
        pass

    @staticmethod
    def create_names_list(names_file_path):
        with open(names_file_path, 'r') as file:
            names = file.read()
            names = names.splitlines()
            print(names)
        return names

    def check_if_login_page(self, page_text):
        w = [word for word in login_words if word in page_text]
        if len(w) > 0:
            return True
        return False

    def url_validator(self, names_list):
        for name in names_list:
            url = self.create_url(name)
            try:
                res = requests.get(url)
                print(res.status_code)
                result = self.check_if_login_page(res.text)
                if result:
                    print(f"{url} is a login page")
                    # send to attacker
                print("=============================================================================")
                self.verified_urls.append(url)
            except requests.ConnectionError:
                pass
