from repository.issue_repository import IssueRepository
from repository.redressal_repository import RedressalRepository
from data.issue import Issue
from data.const import IN_PROGRESS, REDRESSED
from utils.printing import print_issues, print_issue_details, print_redressal_details


class UserFlow:
    def __init__(self, user):
        self.user = user
        self.issue_repo = IssueRepository()
        self.redressal_repo = RedressalRepository()

    def upvote(self, user_id, issue, redressal):
        # upvote issue or redressal
        if issue:
            issue.upvotes.append(user_id)
            self.issue_repo.save(issue)

        elif redressal:
            redressal.upvotes.append(user_id)
            self.redressal_repo.save(redressal)

    def downvote(self, user_id, issue, redressal):
        # downvote issue or redressal
        if issue:
            issue.downvotes.append(user_id)
            self.issue_repo.save(issue)

        elif redressal:
            redressal.downvotes.append(user_id)
            self.read_redressal.append(user_id)

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
                        self.upvote(user_id=self.user.id,
                                    issue=issue, redressal=None)
                    elif action == 2:
                        self.downvote(user_id=self.user.id,
                                      issue=issue, redressal=None)

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
                user_voted = False
                redressal_id = issue.redressal_id

                if redressal_id == None:
                    print('No redressal have been made. Please check again later.')
                    continue

                redressal = self.redressal_repo.get(redressal_id)
                redressal_items = self.redressal_repo.items(redressal)

                # Check user has vote the redressal
                if self.user.id in redressal.upvotes or self.user.id in redressal.downvotes:
                    user_voted = True

                print_redressal_details(issue, redressal, redressal_items)

                if user_voted:
                    if self.user.id in redressal.upvotes:
                        print("You 👍 this redressal.")
                    else:
                        print('You 👎 this redressal.')
                else:
                    print("You haven't voted for this redressal!")
                    print("0) Exit")
                    print("1) Upvote")
                    print("2) Downvote")
                    action = int(input("Action: "))
                    if action == 1:
                        self.upvote(user_id=self.user.id,
                                    issue=None, redressal=redressal)
                    elif action == 2:
                        self.downvote(user_id=self.user.id,
                                      issue=None, redressal=redressal)

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
            1: "ADMIN",
            2: "TRANSPORT",
            3: "ENVIRONMENT",
            4: "EDUCATION"
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
