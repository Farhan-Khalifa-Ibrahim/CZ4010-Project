from dataclasses import dataclass, field
from typing import List, Optional

from utils.time import current_timestamp


@dataclass
class Issue:
    id: str
    '''The issue id.'''
    category: str
    '''Which category the issue belongs to.'''
    status: str
    '''The current status of the redressal.'''
    title: str
    '''The title of the issue.'''
    desc: str
    '''The description of the issue.'''
    upvotes: List[str] = field(default_factory=list)
    '''Signatures of users who upvote the issue.'''
    downvotes: List[str] = field(default_factory=list)
    '''Signatures of users who downvote the issue.'''
    redressal_id: Optional[str] = None
    '''Reference to the redressal.'''
    created_at: float = current_timestamp()

    @property
    def up_count(self) -> int:
        """Number of upvotes."""
        return len(self.upvotes)

    @property
    def down_count(self) -> int:
        """Number of downvotes."""
        return len(self.downvotes)

    @property
    def rejectable(self) -> bool:
        """Returns `true` if this issue can be rejected. The issue can be rejected because
        majority of voters did not agree with the issue.

        Returns:
            bool: `true` if the system should be able to reject this issue.
        """
        if self.down_count == 0:
            return False

        total_votes = self.up_count + self.down_count
        neg_percent = int(self.up_count * 100 / self.down_count)

        return total_votes >= 10 and neg_percent > 70

    @staticmethod
    def from_firestore(id, data):
        return Issue(
            id,
            data['category'],
            data['status'],
            data['title'],
            data['desc'],
            data['upvotes'],
            data['downvotes'],
            data['redressal_id'],
            data['created_at']
        )

    def to_firestore(self):
        return {
            'category': self.category,
            'status': self.status,
            'title': self.title,
            'desc': self.desc,
            'upvotes': self.upvotes,
            'downvotes': self.downvotes,
            'redressal_id': self.redressal_id,
            'created_at': self.created_at
        }
