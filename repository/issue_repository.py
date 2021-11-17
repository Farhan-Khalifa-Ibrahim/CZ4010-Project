from typing import List
from data.issue import Issue
from data.redressal import Redressal
from .firestore_repository import FirestoreRepository


class IssueRepository(FirestoreRepository):
    def __init__(self) -> None:
        super().__init__('issue')

    def _create_from_doc(self, id, data):
        return Issue.from_firestore(id, data)

    def _object_type(self):
        return Issue

    def list_by_issue_votes(self):
        issues = self.list()
        return sorted(issues, key=lambda issue: issue.up_count + issue.down_count, reverse=True)

    def list_by_redressal_votes(self, redressals: List[Redressal]):
        issues = self.list()
        redressal_dict = {}

        for r in redressals:
            redressal_dict[r.id] = r

        return sorted(
            issues, key=lambda i: redressal_dict[i.redressal_id].up_count + redressal_dict[i.redressal_id].down_count, reverse=True)
