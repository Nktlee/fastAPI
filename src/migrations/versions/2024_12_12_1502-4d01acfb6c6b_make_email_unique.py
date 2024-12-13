"""make email unique

Revision ID: 4d01acfb6c6b
Revises: ea49ff53afd7
Create Date: 2024-12-12 15:02:06.975754

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4d01acfb6c6b"
down_revision: Union[str, None] = "ea49ff53afd7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
