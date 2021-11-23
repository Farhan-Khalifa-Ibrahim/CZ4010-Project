from typing import Optional
from data.redressal import Redressal
from repository.issue_repository import IssueRepository
from repository.redressal_repository import RedressalRepository
from repository.user_repository import UserRepository
from data.issue import Issue
from data.const import ADMIN, EDUCATION, ENVIRONMENT, FACILITIES
from utils.printing import print_issues, print_issue_details, print_redressal_details


class UserFlow:
    def __init__(self, user):
        self.user = user
        self.issue_repo = IssueRepository()
        self.redressal_repo = RedressalRepository()
        self.user_repo = UserRepository()

    def upvote(self, issue: Optional[Issue], redressal: Optional[Redressal]):
        # upvote issue or redressal
        if issue:
            issue.upvote(self.user)
            self.issue_repo.save(issue)

            self.user.vote_for(issue)
            self.user_repo.save(self.user)

        elif redressal:
            redressal.upvote(self.user)
            self.redressal_repo.save(redressal)

            self.user.vote_for(redressal)
            self.user_repo.save(self.user)

    def downvote(self, issue: Optional[Issue], redressal: Optional[Redressal]):
        # downvote issue or redressal
        if issue:
            issue.downvote(self.user)
            self.issue_repo.save(issue)

            self.user.vote_for(issue)
            self.user_repo.save(self.user)

        elif redressal:
            redressal.downvote(self.user)
            self.redressal_repo.save(redressal)

            self.user.vote_for(redressal)
            self.user_repo.save(self.user)

    def read_issues(self):
        while True:
            print()
            print('Here are a list of issues, ordered from the most popular.')
            issue_list = self.issue_repo.list_by_issue_votes()

            # print exit and list of issues
            print("0. Exit")
            print_issues(issue_list)

            action = int(input("Action: "))
            if action == 0:
                break

            else:
                issue = issue_list[action-1]

                # Print details of issue
                print()
                user_vote = print_issue_details(issue, self.user)

                # If user has not voted
                if not user_vote:
                    print("0) Exit")
                    print("1) Upvote")
                    print("2) Downvote")
                    action = int(input("Action: "))
                    if action == 1:
                        self.upvote(issue=issue, redressal=None)
                    elif action == 2:
                        self.downvote(issue=issue, redressal=None)

    def read_redressal(self):
        while True:
            print()
            print('For which issue do you want to see the redressal?')
            issue_list = self.issue_repo.list_by_issue_votes()

            # print exit and list of issues
            print("0. Exit")
            print_issues(issue_list)
            action = int(input("Action: "))
            if action == 0:
                break

            else:
                print()

                issue = issue_list[action-1]

                # Get the redressal data for the issue if any.
                redressal_id = issue.redressal_id

                if redressal_id == None:
                    print('No redressal have been made. Please check again later.')
                    continue

                redressal = self.redressal_repo.get(redressal_id)
                redressal_items = self.redressal_repo.items(redressal)

                # Print redressal details
                user_voted = print_redressal_details(
                    issue, redressal, redressal_items, self.user)

                if not user_voted:
                    print("0) Exit")
                    print("1) Upvote")
                    print("2) Downvote")
                    action = int(input("Action: "))
                    if action == 1:
                        self.upvote(issue=None, redressal=redressal)
                    elif action == 2:
                        self.downvote(issue=None, redressal=redressal)

    def write_issue(self):
        print()
        issue_category = ""
        print("Choose the issue category you want to publish")
        print('0) Cancel')
        print("1) Admin")
        print("2) Transport")
        print("3) Environment")
        print("4) Education")

        # User new issue input
        action = int(input("Action: "))

        if action == 0:
            return

        options = {
            1: ADMIN,
            2: FACILITIES,
            3: ENVIRONMENT,
            4: EDUCATION
        }
        issue_category = options[action]
        issue_title = input("Issue title: ")
        issue_description = input("Issue description: ")
        new_issue = Issue(
            id='',  # New data
            category=issue_category,
            status="PENDING",
            title=issue_title,
            desc=issue_description,
            user_id=self.user.encrypted_uid,
        )

        # save issue
        self.issue_repo.save(new_issue)
        print('Your issue has been posted successfully!')

    def main(self):
        while True:
            print("""
What do you want to do?
0. Exit
1. Read issue
2. Read redressal
3. Post issue
            """)
            action = int(input("Action: "))
            if action == 1:
                self.read_issues()
            elif action == 2:
                self.read_redressal()
            elif action == 3:
                self.write_issue()
            elif action == 0:
                print()
                break
