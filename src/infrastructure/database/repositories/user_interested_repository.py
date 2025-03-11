from typing import Optional, List, Dict, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user_interested import UserInterestedDTO
from src.domain.repositories.iuser_interested_repository import IUserInterestedRepository


class UserInterestedRepository(IUserInterestedRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, user_interested: UserInterestedDTO) -> Optional[UserInterestedDTO]:
        """
        Insert a new record into 'user_interesteds'.
        Returns the created UserInterestedDTO or None.
        """
        query = text("""
            INSERT INTO user_interesteds (user_id, interest_id)
            VALUES (:user_id, :interest_id)
            RETURNING id, user_id, interest_id
        """)

        # We can just pass user_interested.dict() if we want to allow None or empty fields
        params = user_interested.dict()
        result = await self._session.execute(query, params)
        row = result.fetchone()

        # NO commit here; rely on UoW
        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserInterestedDTO(**row_dict)
        return None

    async def update(self, record_id: int, user_interested: UserInterestedDTO) -> Optional[UserInterestedDTO]:
        """
        Partially update 'user_interesteds' using filtered_dict to skip None/empty fields.
        """
        payload = user_interested.filtered_dict(exclude_none=True, exclude_empty_str=True)

        # If nothing to update, return the existing record
        if not payload:
            existing = await self.get_by_id(record_id)
            return existing

        # Build dynamic SET clause from the filtered payload
        set_clauses = [f"{key} = :{key}" for key in payload.keys()]
        set_clause_str = ", ".join(set_clauses)

        # Include the ID in the payload for WHERE
        payload["id"] = record_id

        query = text(f"""
            UPDATE user_interesteds
            SET {set_clause_str}
            WHERE id = :id
            RETURNING id, user_id, interest_id
        """)

        result = await self._session.execute(query, payload)
        row = result.fetchone()
        # NO commit here; rely on UoW
        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserInterestedDTO(**row_dict)
        return None

    async def remove(self, record_id: int) -> None:
        """
        Delete a row from 'user_interesteds' by ID.
        """
        query = text("DELETE FROM user_interesteds WHERE id = :id")
        await self._session.execute(query, {"id": record_id})
        # NO commit here; rely on UoW

    async def get_by_id(self, record_id: int) -> Optional[UserInterestedDTO]:
        """
        Fetch a single row by primary key (id).
        """
        query = text("""
            SELECT id, user_id, interest_id
            FROM user_interesteds
            WHERE id = :id
        """)
        result = await self._session.execute(query, {"id": record_id})
        row = result.fetchone()
        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserInterestedDTO(**row_dict)
        return None

    async def get_by_user_id(self, user_id: int) -> Optional[UserInterestedDTO]:
        """
        Fetch the first record matching a user_id.
        If you can have multiple interests per user, change to return a List.
        """
        query = text("""
            SELECT id, user_id, interest_id
            FROM user_interesteds
            WHERE user_id = :user_id
            LIMIT 1
        """)
        result = await self._session.execute(query, {"user_id": user_id})
        row = result.fetchone()
        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserInterestedDTO(**row_dict)
        return None

    async def list(self, filters: Optional[Dict[str, Any]] = None) -> List[UserInterestedDTO]:
        """
        Fetch a list of UserInterestedDTOs, optionally filtered.
        """
        base_query = "SELECT id, user_id, interest_id FROM user_interesteds"
        params = {}

        if filters:
            clauses = []
            for key, value in filters.items():
                clauses.append(f"{key} = :{key}")
                params[key] = value
            if clauses:
                base_query += " WHERE " + " AND ".join(clauses)

        query = text(base_query)
        result = await self._session.execute(query, params)
        rows = result.fetchall()

        return [
            UserInterestedDTO(**dict(zip(row.keys(), row)))
            for row in rows
        ]
