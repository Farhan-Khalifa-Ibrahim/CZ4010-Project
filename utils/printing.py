from datetime import datetime
from typing import List
from data.const import REDRESSED


from data.issue import Issue
from data.redressal import Redressal, RedressalItem


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
            f"{num}) {issue.title} ({issue.up_count} 👍 {issue.down_count} 👎) ({issue.status})"
        )


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
        for item in items:
            timing = datetime.strftime(item.created_dt, '%d %B %Y, %H:%M')
            print(f'({timing}) {item.message}')
