from .firestore_repository import FirestoreRepository
from data.redressal import Redressal, RedressalItem


class RedressalRepository(FirestoreRepository):
    def __init__(self) -> None:
        super().__init__('redressal')

    def _object_type(self):
        return Redressal

    def create_from_doc(self, id: str, data: dict):
        return Redressal.from_firestore(id, data)


class RedressalItemRepository(FirestoreRepository):
    def __init__(self) -> None:
        super().__init__('redressal-item')

    def _object_type(self):
        return RedressalItem

    def _create_from_doc(self, id: str, data: dict):
        return RedressalItem.from_firestore(id, data)
