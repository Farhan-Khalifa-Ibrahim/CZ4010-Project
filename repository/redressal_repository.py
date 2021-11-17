from typing import List
from data.user import User
from .firestore_repository import FirestoreRepository
from data.redressal import Redressal, RedressalItem


class RedressalItemRepository(FirestoreRepository):
    def __init__(self) -> None:
        super().__init__('redressal-item')

    def _object_type(self):
        return RedressalItem

    def _create_from_doc(self, id: str, data: dict):
        return RedressalItem.from_firestore(id, data)


class RedressalRepository(FirestoreRepository):
    def __init__(self) -> None:
        super().__init__('redressal')

        self.item_repo = RedressalItemRepository()

    def _object_type(self):
        return Redressal

    def _create_from_doc(self, id: str, data: dict):
        return Redressal.from_firestore(id, data)

    def add_redressal_item(self, redressal: Redressal, message: str, user: User):
        # Create a new item
        new_item = RedressalItem(id='', message=message, signed_by=user.uid)
        new_item = self.item_repo.save(new_item)
        new_item_id = new_item.id

        # Add item to redressal
        redressal.item_ids.append(new_item_id)
        self.save(redressal)

    def items(self, redressal: Redressal) -> List[RedressalItem]:
        items = list(
            map(lambda id: self.item_repo.get(id), redressal.item_ids))

        return sorted(items, key=lambda item: item.created_at)

    def clear_votes(self, redressal: Redressal):
        redressal.upvotes.clear()
        redressal.downvotes.clear()
        self.save(redressal)
