from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from utils.time import current_timestamp, from_timestamp


@dataclass
class Redressal:
    id: str
    '''The redressal id.'''
    created_at: float = current_timestamp()
    '''The timestamp the redressal was created in POSIX.'''
    item_ids: List[str] = field(default_factory=list)
    '''The ids of the updates regarding this addressal.'''
    upvotes: List[str] = field(default_factory=list)
    '''Signatures of users who upvote the redressal.'''
    downvotes: List[str] = field(default_factory=list)
    '''Signatures of users who downvote the redressal.'''

    @property
    def up_count(self) -> int:
        return len(self.upvotes)

    @property
    def down_count(self) -> int:
        return len(self.downvotes)

    @property
    def complaint(self):
        """Returns `true` if this redressal needs to be readdressed. The redressal can be rejected because
        majority of voters did not agree with the redressal.

        Returns:
            bool: `true` if the system should notify admin to reconsider this redressal.
        """
        total_votes = self.up_count + self.down_count
        neg_percent = int(self.up_count * 100 / self.down_count)

        return total_votes >= 10 and neg_percent > 70

    @staticmethod
    def from_firestore(id, data):
        return Redressal(
            id=data['id'],
            created_at=data['created_at'],
            item_ids=data['item_ids'],
            upvotes=data['upvotes'],
            downvotes=data['downvotes']
        )

    def to_firestore(self):
        return {
            'created_at': self.created_at,
            'item_ids': self.item_ids,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes
        }


@dataclass
class RedressalItem:
    """
    This class represents an item in the redressal log.
    """

    id: str
    '''The id of this redressal item.'''
    message: str
    '''The message to be displayed to the user.'''
    signed_by: str
    '''The signature of the admin that adds the item.'''
    created_at: float = current_timestamp()
    '''The timestamp in POSIX.'''

    @property
    def created_dt(self) -> datetime:
        return from_timestamp(self.created_at)

    @staticmethod
    def from_firestore(id, data):
        return RedressalItem(
            id=id,
            message=data['message'],
            signed_by=data['signed_by'],
            created_at=data['created_at']
        )

    def to_firestore(self):
        return {
            'message': self.message,
            'signed_by': self.signed_by,
            'created_at': self.created_at
        }