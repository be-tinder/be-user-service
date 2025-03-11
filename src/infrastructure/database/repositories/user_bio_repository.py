from typing import Optional, List, Dict, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user_bio import UserBioDTO
from src.domain.repositories.iuser_bio_repository import IUserBioRepository


class UserBioRepository(IUserBioRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, user_bio: UserBioDTO) -> Optional[UserBioDTO]:
        """
        Insert a new row into 'user_bios'.
        Returns the created UserBioDTO or None.
        """
        query = text("""
            INSERT INTO user_bios (
                bio,
                height,
                goals_relation,
                languages,
                zodiac_sign,
                education,
                children_preference,
                user_id
            )
            VALUES (
                :bio,
                :height,
                :goals_relation,
                :languages,
                :zodiac_sign,
                :education,
                :children_preference,
                :user_id
            )
            RETURNING 
                id,
                bio,
                height,
                goals_relation,
                languages,
                zodiac_sign,
                education,
                children_preference,
                user_id
        """)

        result = await self._session.execute(query, user_bio.dict())
        row = result.fetchone()

        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserBioDTO(**row_dict)
        return None

    async def update(self, user_bio_id: int, user_bio: UserBioDTO) -> Optional[UserBioDTO]:
        """
        Partially update 'user_bios' using filtered_dict
        so that only non-empty / non-None fields are updated.
        """
        payload = user_bio.filtered_dict(exclude_none=True, exclude_empty_str=True)

        if not payload:
            existing = await self.get_by_id(user_bio_id)
            return existing

        set_clauses = [f"{column} = :{column}" for column in payload.keys()]
        set_clause_str = ", ".join(set_clauses)

        payload["id"] = user_bio_id

        query = text(f"""
            UPDATE user_bios
            SET {set_clause_str}
            WHERE id = :id
            RETURNING 
                id,
                bio,
                height,
                goals_relation,
                languages,
                zodiac_sign,
                education,
                children_preference,
                user_id
        """)

        result = await self._session.execute(query, payload)
        row = result.fetchone()

        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserBioDTO(**row_dict)
        return None

    async def remove(self, user_bio_id: int) -> None:
        """
        Delete a row in 'user_bios' by ID.
        """
        query = text("DELETE FROM user_bios WHERE id = :id")
        await self._session.execute(query, {"id": user_bio_id})

    async def get_by_id(self, user_bio_id: int) -> Optional[UserBioDTO]:
        """
        Fetch a single row by primary key ID.
        """
        query = text("""
            SELECT
                id,
                bio,
                height,
                goals_relation,
                languages,
                zodiac_sign,
                education,
                children_preference,
                user_id
            FROM user_bios
            WHERE id = :id
        """)
        result = await self._session.execute(query, {"id": user_bio_id})
        row = result.fetchone()

        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserBioDTO(**row_dict)
        return None

    async def get_by_user_id(self, user_id: int) -> Optional[UserBioDTO]:
        """
        Fetch a single user_bio by the user's ID.
        If each user has only one bio, this returns it or None.
        If user_bios can be multiple per user, adjust to return a list.
        """
        query = text("""
            SELECT
                id,
                bio,
                height,
                goals_relation,
                languages,
                zodiac_sign,
                education,
                children_preference,
                user_id
            FROM user_bios
            WHERE user_id = :user_id
            LIMIT 1
        """)
        result = await self._session.execute(query, {"user_id": user_id})
        row = result.fetchone()

        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserBioDTO(**row_dict)
        return None

    async def list(self, filters: Optional[Dict[str, Any]] = None) -> List[UserBioDTO]:
        """
        Return a list of UserBioDTO objects, optionally filtered by criteria.
        """
        base_query = """
            SELECT
                id,
                bio,
                height,
                goals_relation,
                languages,
                zodiac_sign,
                education,
                children_preference,
                user_id
            FROM user_bios
        """

        query_params = {}
        if filters:
            clauses = []
            for key, value in filters.items():
                clauses.append(f"{key} = :{key}")
                query_params[key] = value

            if clauses:
                base_query += " WHERE " + " AND ".join(clauses)

        query = text(base_query)
        result = await self._session.execute(query, query_params)
        rows = result.fetchall()

        return [
            UserBioDTO(**dict(zip(row.keys(), row)))
            for row in rows
        ]
