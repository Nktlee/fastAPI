"""edit title column in rooms to unique

Revision ID: 6c3932a75253
Revises: 4d01acfb6c6b
Create Date: 2024-12-18 15:59:01.863433

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6c3932a75253"
down_revision: Union[str, None] = "4d01acfb6c6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "rooms", ["title"])


def downgrade() -> None:
    op.drop_constraint(None, "rooms", type_="unique")
