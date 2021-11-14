import firebase_admin
from firebase_admin import credentials
from repository.issue_repository import IssueRepository
from repository.redressal_repository import RedressalRepository


class user_class:
    def __init__(self, user):
        self.user = user
        cred = credentials.Certificate('service_account.json')
        firebase_admin.initialize_app(cred)
        issue_repo = IssueRepository()
        redressal_repo = RedressalRepository()

    def read_issues(self):
        pass

    def read_readdresals(self):
        pass

    def write_issue(self):
        pass

    def main(self):
        while True:
            print("""
                What do you want to do?
                1. Read issues
                2. Read readdresal
                3. Post issue
                0. Exit
            """)
            action = int(input("Action: "))
            if action == 1:
                self.read_issues()
            elif action == 2:
                self.read_readdresals()
            elif action == 3:
                self.write_issue()
            elif action == 0:
                break
