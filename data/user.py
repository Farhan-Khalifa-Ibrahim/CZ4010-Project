from dataclasses import dataclass, field
from typing import Optional, Set, Union

from crypto import encrypt
from data.issue import Issue
from data.redressal import Redressal


@dataclass
class User:
    id: str
    """Firestore document id. Use `uid` instead."""
    uid: str
    """The user's id."""
    is_admin: bool = False
    """Whether this user is an admin or a public user."""
    category: Optional[str] = None
    """If the user is an admin, this value will be one of the 
    issue category. Otherwise this is `None`."""
    voted_items: Set[str] = field(default_factory=set)
    """Entity ids that the user has voted for."""

    @property
    def encrypted_uid(self) -> str:
        """The user id encrypted with Fernet."""
        return encrypt(self.uid.encode()).decode()

    @staticmethod
    def from_firestore(id, data):
        return User(
            id=id,
            uid=data['uid'],
            is_admin=data['is_admin'],
            category=data.get('category'),
            voted_items=set(data.get('voted_items', []))
        )

    def to_firestore(self):
        general_data = {
            'uid': self.uid,
            'is_admin': self.is_admin,
            'voted_items': self.voted_items,
        }

        if not self.category is None:
            general_data['category'] = self.category

        return general_data

    def vote_for(self, entity: Union[Issue, Redressal]):
        self.voted_items.add(entity.id)

    def has_voted(self, entity: Union[Issue, Redressal]) -> bool:
        return entity.id in self.voted_items
