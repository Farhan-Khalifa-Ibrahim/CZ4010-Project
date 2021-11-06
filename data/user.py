from dataclasses import dataclass
from os import stat
from typing import Optional


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

    @staticmethod
    def from_firestore(id, data):
        return User(
            id=id,
            uid=data['uid'],
            is_admin=data['is_admin'],
            category=data.get('category')
        )

    def to_firestore(self):
        general_data = {
            'uid': self.uid,
            'is_admin': self.is_admin
        }

        if not self.category is None:
            general_data['category'] = self.category

        return general_data
