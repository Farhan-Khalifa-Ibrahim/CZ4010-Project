from datetime import datetime
from typing import List
from data.const import REDRESSED


from data.issue import Issue
from data.redressal import Redressal, RedressalItem
from data.user import User


def print_issues(issues: List[Issue]):
    """Prints a list of issues.

    Example:
    1) Bis NTU Lambat (50 👍 3 👎) (IN PROGRESS)
    2) Bis NTU Lambat (50 👍 3 👎) (IN PROGRESS)
    3) Bis NTU Lambat (50 👍 3 👎) (IN PROGRESS)

    Args:
        issues (List[Issue]): The list of issues.
    """

    # Sort issues based on the votes
    sorted_issues = sorted(issues, key=lambda i: i.up_count + i.down_count)

    for num, issue in enumerate(sorted_issues, start=1):
        print(
            f"{num}) {issue.title} ({issue.up_count} 👍 {issue.down_count} 👎) ({issue.status})"
        )


def print_redressed_issues(issues: List[Issue], redressal: List[Redressal]):
    redressal_dict = {}

    for r in redressal:
        redressal_dict[r.id] = r

    sorted_issues = sorted(
        issues, key=lambda i: redressal_dict[i.redressal_id].up_count + redressal_dict[i.redressal_id].down_count)

    for num, issue in enumerate(sorted_issues, start=1):
        r = redressal_dict[issue.redressal_id]

        print(
            f"{num}) Redressal for '{issue.title}' ({r.up_count} 👍 {r.down_count} 👎)"
        )


def print_issue_details(issue: Issue, user: User):
    print("Title: " + issue.title)
    print("Description: " + issue.desc)
    print("Category: " + issue.category)
    print("Status: " + issue.status)
    print(f"Votes: {len(issue.upvotes)} 👍 {len(issue.downvotes)} 👎")

    if not user.is_admin:
        if user.uid in issue.upvotes:
            print('You 👍 this issue')
        elif user.uid in issue.downvotes:
            print("You 👎 this issue")
        else:
            print("You have not voted for this issue.")


def print_redressal_items(items: List[RedressalItem]):
    sorted_items = sorted(items, key=lambda i: i.created_at)

    for item in sorted_items:
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
