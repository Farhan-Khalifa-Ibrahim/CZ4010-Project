from data.redressal import Redressal
from repository.issue_repository import IssueRepository
from repository.redressal_repository import RedressalRepository
from data.const import IN_PROGRESS, PENDING, REDRESSED, REJECTED
from utils.printing import print_issue_details, print_issues, print_redressal_details, print_redressal_items, print_redressed_issues


class AdminFlow:
    def __init__(self, user) -> None:
        self.user = user

        self.issue_repo = IssueRepository()
        self.red_repo = RedressalRepository()

    @property
    def issues_for_category(self):
        """Returns issues that are the same category as the admin user's category."""
        issues = self.issue_repo.list_by_issue_votes()
        return list(filter(lambda i: i.category == self.user.category, issues))

    def connect_redressal(self, issue):
        redressal_id = input(
            'Input the redressal id that has solved this issue: ')

        try:
            self.red_repo.get(redressal_id)
        except KeyError:
            print(f"The id {redressal_id} doesn't exist!")
            return

        # Link to other redressal
        issue.redressal_id = redressal_id
        # Mark the issue as redressed
        issue.status = REDRESSED
        self.issue_repo.save(issue)

    def reject_issue(self, issue):
        decision = input(
            'Are you sure you want to reject this issue (Y/N)? ').lower()

        if decision == 'y':
            issue.status = REJECTED
            self.issue_repo.save(issue)

    def log_redressal_activity(self, redressal_id):
        redressal = self.red_repo.get(redressal_id)
        items = self.red_repo.items(redressal)

        print_redressal_items(items)
        message = input('Enter new redressal message (0 to cancel): ')
        if message == '0':
            return

        # Save the item
        self.red_repo.add_redressal_item(redressal, message, self.user)

    def change_status(self, issue_id):
        issue = self.issue_repo.get(issue_id)
        print()
        print(f'Current status: {issue.status}')

        if issue.status == REDRESSED:
            print("This issue have been redressed! You can't change the status.")
        elif issue.status == PENDING:
            option = input(f'Change status to {IN_PROGRESS}? (Y/N) ').lower()

            if option == 'y':
                issue.status = IN_PROGRESS

                # Create redressal for this issue
                redressal = Redressal(id='')
                redressal = self.red_repo.save(redressal)

                self.red_repo.add_redressal_item(
                    redressal, 'Redressal in progress', self.user)

                # Update the issue
                issue.redressal_id = redressal.id
                self.issue_repo.save(issue)
        elif issue.status == IN_PROGRESS:
            option = input(f'Change status to {REDRESSED}? (Y/N) ').lower()

            if option == 'y':
                issue.status = REDRESSED
                self.issue_repo.save(issue)

                # Log update
                redressal = self.red_repo.get(issue.redressal_id)
                self.red_repo.add_redressal_item(
                    redressal, 'Issue resolved', self.user)

    def get_actions_for_issue(self, issue):
        actions = ['Back']
        if issue.status != REDRESSED:
            actions.append('Change status')

        if issue.status == IN_PROGRESS:
            actions.append('Log redressal activity')

        if issue.status == PENDING or issue.status == IN_PROGRESS:
            actions.append('Solve with other redressal')

        if issue.rejectable:
            actions.append('Reject issue')

        return actions

    def handle_issue(self, issue_id):
        while True:
            issue = self.issue_repo.get(issue_id)
            print()
            print_issue_details(issue, self.user)

            actions = self.get_actions_for_issue(issue)

            for i, a in enumerate(actions):
                print(f'{i}. {a}')

            action = input('Action: ')

            if action == '0':
                break

            try:
                int_action = int(action)

                if int_action >= len(actions):
                    continue
            except ValueError:
                continue

            action_str = actions[int_action]
            if action_str == 'Change status':
                self.change_status(issue_id)
            elif action_str == 'Log redressal activity':
                self.log_redressal_activity(issue.redressal_id)
            elif action_str == 'Reject issue':
                self.reject_issue(issue)
            elif action_str == 'Solve with other redressal':
                self.connect_redressal(issue)

    def list_issues(self):
        while True:
            issues = self.issues_for_category
            print('0. Back')
            print_issues(issues)
            action = input("Which issue do you want to redress? ")

            if action == '0':
                break
            else:
                try:
                    issue_index = int(action) - 1
                except ValueError:
                    continue

                self.handle_issue(issues[issue_index].id)

    def view_redressed(self, issue, redressal):
        print_redressal_details(
            issue, redressal, self.red_repo.items(redressal), self.user)

        if redressal.complaint:
            print('Users are not satisfied with the redressal!')

            print()
            print('0. Back')
            print('1. Re-redress')

            action = input('Action: ')
            if action == '1':
                # Back to in progress
                issue.status = IN_PROGRESS
                self.issue_repo.save(issue)

                # Log the activity
                self.red_repo.add_redressal_item(
                    redressal, "Redressal re-opened", self.user)

                # Remove the votes for redressal
                self.red_repo.clear_votes(redressal)

        else:
            print('Users are satisfied with the redressal. No actions required.')

    def list_redressed(self):
        while True:
            redressed = list(filter(lambda issue: issue.status ==
                                    REDRESSED, self.issues_for_category))

            if len(redressed) > 0:
                redressed = self.issue_repo.list_by_redressal_votes(
                    self.red_repo.list()
                )
                print(
                    '\nHere are all issues that have been redressed and the corresponding response from users.')
                print('0. Back')
                print_redressed_issues(redressed, self.red_repo)
                action = input('Choose redressal to view: ')

                if action == '0':
                    break
                else:
                    try:
                        index = int(action) - 1
                    except ValueError:
                        continue

                    issue = redressed[index]
                    redressal = self.red_repo.get(issue.redressal_id)
                    self.view_redressed(issue, redressal)

            else:
                print('No redressed issue!')
                break

    def main(self):
        while True:
            print(f'\nYou are responsible for category: {self.user.category}')

            # Filter by category
            new_issues = list(
                filter(lambda issue: issue.status == PENDING, self.issues_for_category))

            in_progress_issues = list(
                filter(lambda issue: issue.status == IN_PROGRESS, self.issues_for_category))

            if len(new_issues) > 0:
                print(f"{len(new_issues)} new issues")

            if len(in_progress_issues) > 0:
                print(f'{len(in_progress_issues)} issues in progress')

            print()
            print("0. Back")
            print("1. List Issue")
            print("2. List Redressed")

            action = input('Action: ')

            if action == '0':
                print()
                break
            elif action == '1':
                print()
                self.list_issues()
            elif action == '2':
                print()
                self.list_redressed()
