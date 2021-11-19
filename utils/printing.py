from datetime import datetime
from typing import List
from data.const import REDRESSED


from data.issue import Issue
from data.redressal import Redressal, RedressalItem
from data.user import User
from repository.redressal_repository import RedressalRepository


def print_issues(issues: List[Issue]):
    """Prints a list of issues.

    Example:
    1) Bis NTU Lambat (50 👍 3 👎) (IN PROGRESS)
    2) Bis NTU Lambat (50 👍 3 👎) (IN PROGRESS)
    3) Bis NTU Lambat (50 👍 3 👎) (IN PROGRESS)

    Args:
        issues (List[Issue]): The list of issues.
    """

    for num, issue in enumerate(issues, start=1):
        print(
            f"{num}. {issue.title} ({issue.up_count} 👍 {issue.down_count} 👎) ({issue.status})"
        )


def print_redressed_issues(issues: List[Issue], repo: RedressalRepository):
    for num, issue in enumerate(issues, start=1):
        r = repo.get(issue.redressal_id)

        print(
            f"{num}. Redressal for '{issue.title}' ({r.up_count} 👍 {r.down_count} 👎)"
        )


def print_issue_details(issue: Issue, user: User) -> bool:
    """Prints the details of the issue and return `True` if the user has voted for the issue.

    Args:
        issue (Issue): The issue to be printed.
        user (User): The current user signed in.

    Returns:
        bool: `True` if the user has voted for the issue. Not applicable for admin users.
    """
    print("Title: " + issue.title)
    print("Description: " + issue.desc)
    print("Category: " + issue.category)
    print("Status: " + issue.status)
    print(f"Votes: {len(issue.upvotes)} 👍 {len(issue.downvotes)} 👎")

    if not user.is_admin:
        print()

        if user.uid in issue.upvotes:
            print('You 👍 this issue')
            return True
        elif user.uid in issue.downvotes:
            print("You 👎 this issue")
            return True
        else:
            print("You have not voted for this issue.")
            return False

    return False


def print_redressal_items(items: List[RedressalItem]):
    for item in items:
        timing = datetime.strftime(item.created_dt, '%d %B %Y, %H:%M')
        print(f'({timing}) {item.message}')


def print_redressal_details(issue: Issue, redressal: Redressal, items: List[RedressalItem]):
    # Redressal id: asjdkasduhid
    # Issue: Bis NTU lambat
    # Status: REDRESSED
    # Votes: 50 👍 3 👎

    # (4 Nov 2021 07:00) Admin is taking action -> waktu status diganti jd in progress
    # (4 Nov 2021 08:00) Redirected to supervisor
    # (4 Nov 2021 10:00) Communicating to Tong Tar Transport
    # (4 Nov 2021 11:00) Action completed
    print(f"Redressal ID: {redressal.id}")
    print(f"Issue: {issue.title}")
    print(f'Status: {issue.status}')

    if issue.status == REDRESSED:
        print(
            f'Redressal votes: {redressal.up_count} 👍 {redressal.down_count} 👎'
        )

    if len(items) != 0:
        print()
        print_redressal_items(items)
