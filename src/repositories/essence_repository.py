from pprint import pprint
from typing import List, Any

from sqlalchemy import select
from sqlalchemy.orm import selectinload, aliased, joinedload, contains_eager

from .sql_alchemy_repository import SQLAlchemyRepository
from src.models.check_model import UserEssence, Check
from ..services.checks.schemas.check_get_schema import FilteringParams


class UserEssenceRepository(SQLAlchemyRepository):
    """UserEssence repository class."""

    model = UserEssence

    async def get_user_essence_id(self, user_id: int) -> UserEssence | None:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_essence_by_user_id(
        self,
        user_id: int,
        filter_params: FilteringParams = FilteringParams(),
        sorting_rule: str = "asc",
        limit: int | None = None,
        offset: int | None = None,
    ) -> UserEssence | None:
        pprint(filter_params)

        # Use an alias for Check to join and apply conditions
        check_alias = aliased(Check)
        stmt = select(self.model).where(self.model.user_id == user_id).distinct()

        # Join with alias and apply eager loading
        stmt = stmt.join(check_alias, self.model.user_checks).options(
            contains_eager(self.model.user_checks, alias=check_alias)
        )

        if filter_params.start_date:
            stmt = stmt.filter(check_alias.check_datetime >= filter_params.start_date)
        if filter_params.end_date:
            stmt = stmt.filter(check_alias.check_datetime <= filter_params.end_date)
        if filter_params.total_price and filter_params.total_price_filtering_rule:
            if filter_params.total_price_filtering_rule == "gt":
                stmt = stmt.filter(check_alias.check_total_price > filter_params.total_price)
            elif filter_params.total_price_filtering_rule == "ge":
                stmt = stmt.filter(check_alias.check_total_price >= filter_params.total_price)
            elif filter_params.total_price_filtering_rule == "lt":
                stmt = stmt.filter(check_alias.check_total_price < filter_params.total_price)
            elif filter_params.total_price_filtering_rule == "le":
                stmt = stmt.filter(check_alias.check_total_price <= filter_params.total_price)
        if filter_params.purchase_type:
            stmt = stmt.filter(check_alias.check_purchasing_method == filter_params.purchase_type)

        if sorting_rule == "asc":
            stmt = stmt.order_by(check_alias.check_datetime.asc())
        elif sorting_rule == "desc":
            stmt = stmt.order_by(check_alias.check_datetime.desc())
        stmt = stmt.limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        user_essence = result.unique().scalar_one_or_none()

        return user_essence
