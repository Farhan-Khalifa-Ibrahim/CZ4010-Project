import firebase_admin
from firebase_admin import credentials
from repository.issue_repository import IssueRepository
from repository.redressal_repository import RedressalRepository
from data.issue import Issue


class user_class:
    def __init__(self, user):
        self.user = user
        self.issue_repo = IssueRepository()
        self.redressal_repo = RedressalRepository()
        self.new_vote_issue_ids = set()
        self.new_vote_redressal_ids = set()

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
        issue_list = self.issue_repo.list()
        while True:
            # print exit and list of issues
            print("0) Exit")
            for index, issue in enumerate(issue_list):
                upvotes = len(issue.upvotes)
                downvotes = len(issue.downvotes)
                print(str(index+1)+") "+issue.title, end=" ")
                print("("+str(upvotes)+"👍"+str(downvotes)+"👎"+")", end=" ")
                print("("+str(issue.status)+")")
            action = int(input("Action: "))

            if action == 0:
                break

            else:
                issue = issue_list[action-1]
                user_vote = False
                if self.user.id in issue.upvotes or self.user.id in issue.downvotes or issue.id in self.new_vote_issue_ids:
                    user_vote = True

                # print details of the issue
                print("Title: "+issue.title)
                print("Description: "+issue.desc)
                print("Category: ", issue.category)
                print("Status: ", issue.status)
                print("votes: "+str(issue.upvotes)+"👍"+str(issue.downvotes)+"👎")

                # If use already voted
                if user_vote:
                    print("You have voted for this issue")
                    print("0) Exit")
                    action = int(input("Action: "))
                    if action == 0:
                        pass

                else:
                    print("You haven't voted for this issue")
                    print("0) Exit")
                    print("1) Upvote")
                    print("2) Downvote")
                    action = int(input("Action: "))
                    if action == 1:
                        self.upvote(user_id=self.user.id,
                                    issue=issue, redressal=None)
                        # add issue id to new_vote_issue_ids
                        self.new_vote_issue_ids.add(issue.id)
                    elif action == 2:
                        self.downvote(user_id=self.user.id,
                                      issue=issue, redressal=None)
                        # add issue id to new_vote_issue_ids
                        self.new_vote_issue_ids.add(issue.id)
                    else:
                        pass

    def read_redressal(self):
        issue_list = self.issue_repo.list()
        while True:
            # print exit and list of issues
            print("0) Exit")
            for index, issue in enumerate(issue_list):
                upvotes = len(issue.upvotes)
                downvotes = len(issue.downvotes)
                print(str(index+1)+") "+issue.title, end=" ")
                print("("+str(upvotes)+"👍"+str(downvotes)+"👎"+")", end=" ")
                print("("+str(issue.status)+")")
            action = int(input("Action: "))

            if action == 0:
                break

            else:
                issue = issue_list[action-1]
                user_voted = False
                redressal_id = issue.redressal_id
                if redressal_id != None:
                    redressal = self.redressal_repo.get(redressal_id)

                # Check user has vote the redressal
                if redressal_id in self.new_vote_redressal_ids or self.user.id in redressal.upvotes or self.user.id in redressal.downvotes:
                    user_voted = True

                """
                Issue: Bis NTU lambat
                Status: REDRESSED
                Redressal id: asjdkasduhid
                Votes: 50 👍 3 👎
                (4 Nov 2021 07:00) Admin is taking action -> waktu status diganti jd in progress
                (4 Nov 2021 08:00) Redirected to supervisor
                (4 Nov 2021 10:00) Communicating to Tong Tar Transport
                (4 Nov 2021 11:00) Action completed
                """

                print("Issue: "+issue.title)
                print("Status: "+issue.status)
                print("Redressal id: "+redressal_id)
                print("votes: "+str(redressal.upvotes)+"👍"+str(redressal.downvotes)+"👎")

                # TODO: List Redressal Timeline

                if user_voted:
                    print("You have voted for this issue")
                    print("0) Exit")
                    action = int(input("Action: "))
                    if action == 0:
                        pass

                else:
                    print("You haven't voted for this issue")
                    print("0) Exit")
                    print("1) Upvote")
                    print("2) Downvote")
                    action = int(input("Action: "))
                    if action == 1:
                        self.upvote(user_id=self.user.id,
                                    issue=None, redressal=redressal)
                        # add issue id to new_vote_redressal_ids
                        self.new_vote_redressal_ids.add(redressal_id)
                    elif action == 2:
                        self.downvote(user_id=self.user.id,
                                      issue=None, redressal=redressal)
                        # add issue id to new_vote_redressal_ids
                        self.new_vote_redressal_ids.add(redressal_id)
                    else:
                        pass

    def write_issue(self):
        issue_cateogry = ""
        print("Choose the issue category you want to publish")
        print("1) Admin")
        print("2) Transport")
        print("3) Environment")
        print("4) Education")

        # User new issue input
        action = int(input("Action: "))
        options = {
            1: "ADMIN",
            2: "TRANSPORT",
            3: "ENVIRONMENT",
            4: "EDUCATION"
        }
        issue_cateogry = options[action]
        issue_title = input("Issue title: ")
        issue_description = input("Issue description: ")
        new_issue = Issue(
            id='',  # New data
            category=issue_cateogry,
            status="PENDING",
            title=issue_title,
            desc=issue_description,
        )

        # save issue
        self.issue_repo.save(new_issue)

    def main(self):
        while True:
            print("""
What do you want to do?
1. Read issue
2. Read redressal
3. Post issue
0. Exit
            """)
            action = int(input("Action: "))
            if action == 1:
                self.read_issues()
            elif action == 2:
                self.read_redressal()
            elif action == 3:
                self.write_issue()
            elif action == 0:
                break
