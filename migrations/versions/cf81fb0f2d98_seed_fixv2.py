"""seed fixv2

Revision ID: cf81fb0f2d98
Revises: 4afe0d625fd8
Create Date: 2024-05-04 21:14:19.130028

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cf81fb0f2d98"
down_revision: Union[str, None] = "4afe0d625fd8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("checks_check_stock_id_fkey", "checks", type_="foreignkey")
    op.drop_column("checks", "check_stock_id")
    op.add_column("sold_products", sa.Column("sold_stock_id", sa.Integer(), nullable=False))
    op.drop_constraint("sold_products_sold_check_id_fkey", "sold_products", type_="foreignkey")
    op.create_foreign_key(None, "sold_products", "checks", ["sold_check_id"], ["id"], ondelete="RESTRICT")
    op.create_foreign_key(None, "sold_products", "stock", ["sold_stock_id"], ["id"], ondelete="SET NULL")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "sold_products", type_="foreignkey")
    op.drop_constraint(None, "sold_products", type_="foreignkey")
    op.create_foreign_key("sold_products_sold_check_id_fkey", "sold_products", "checks", ["sold_check_id"], ["id"])
    op.drop_column("sold_products", "sold_stock_id")
    op.add_column("checks", sa.Column("check_stock_id", sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key(
        "checks_check_stock_id_fkey", "checks", "stock", ["check_stock_id"], ["id"], ondelete="SET NULL"
    )
    # ### end Alembic commands ###
