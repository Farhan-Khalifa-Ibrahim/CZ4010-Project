from dataclasses import dataclass, field
from typing import Optional, Set

from utils.time import current_timestamp


@dataclass
class Issue:
    id: str
    '''The issue id.'''
    user_id: str
    '''The encrypted user id that submits this issue.'''
    category: str
    '''Which category the issue belongs to.'''
    status: str
    '''The current status of the redressal.'''
    title: str
    '''The title of the issue.'''
    desc: str
    '''The description of the issue.'''
    upvotes: Set[str] = field(default_factory=set)
    '''Encrypted user ids who upvote the issue.'''
    downvotes: Set[str] = field(default_factory=set)
    '''Encrypted user ids who downvote the issue.'''
    redressal_id: Optional[str] = None
    '''Reference to the redressal.'''
    created_at: float = current_timestamp()
    '''When the issue was created.'''

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
            id=id,
            category=data['category'],
            status=data['status'],
            title=data['title'],
            desc=data['desc'],
            upvotes=set(data['upvotes']),
            downvotes=set(data['downvotes']),
            redressal_id=data['redressal_id'],
            created_at=data['created_at'],
            user_id=data['user_id']
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
            'created_at': self.created_at,
            'user_id': self.user_id
        }

    def upvote(self, user):
        """Upvote this issue."""
        self.upvotes.add(user.encrypted_uid)

    def downvote(self, user):
        """Downvote this issue."""
        self.downvotes.add(user.encrypted_uid)
