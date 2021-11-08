from data.issue import Issue
from .firestore_repository import FirestoreRepository


class IssueRepository(FirestoreRepository):
    def __init__(self) -> None:
        super().__init__('issue')

    def _create_from_doc(self, id, data):
        return Issue.from_firestore(id, data)

    def _object_type(self):
        return Issue
