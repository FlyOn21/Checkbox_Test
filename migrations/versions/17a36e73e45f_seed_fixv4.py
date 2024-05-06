"""seed fixv4

Revision ID: 17a36e73e45f
Revises: eb0fe0bb4e51
Create Date: 2024-05-05 20:09:39.987705

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "17a36e73e45f"
down_revision: Union[str, None] = "eb0fe0bb4e51"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("sold_products", sa.Column("sold_product_id", sa.Uuid(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("sold_products", "sold_product_id")
    # ### end Alembic commands ###
