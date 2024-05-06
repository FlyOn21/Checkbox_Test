"""seed fix

Revision ID: 4afe0d625fd8
Revises: 12f85798732a
Create Date: 2024-05-04 20:16:42.763823

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4afe0d625fd8"
down_revision: Union[str, None] = "12f85798732a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "checks",
        "check_purchasing_method",
        existing_type=sa.VARCHAR(length=4),
        type_=sa.Enum("cashless", "cash", native_enum=False),
        existing_nullable=False,
    )
    op.create_unique_constraint(None, "products", ["product_title"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "products", type_="unique")
    op.alter_column(
        "checks",
        "check_purchasing_method",
        existing_type=sa.Enum("cashless", "cash", native_enum=False),
        type_=sa.VARCHAR(length=4),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
