from .firestore_repository import FirestoreRepository
from data.user import User


class UserRepository(FirestoreRepository):
    def __init__(self) -> None:
        super().__init__('user')

    def _object_type(self):
        return User

    def _create_from_doc(self, id: str, data: dict):
        return User.from_firestore(id, data)
