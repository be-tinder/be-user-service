from typing import Optional, List, Dict, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.interest import InterestDTO
from src.domain.repositories.iinterest_repository import IInterestRepository


class InterestRepository(IInterestRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, interest: InterestDTO) -> Optional[InterestDTO]:
        """
        Insert a new row into the 'interests' table.
        Returns the created InterestDTO or None.
        """
        query = text("""
            INSERT INTO interests (name)
            VALUES (:name)
            RETURNING id, name
        """)
        # No 'commit' here; rely on UoW for commit
        result = await self._session.execute(query, interest.filtered_dict())
        row = result.fetchone()
        if row:
            return InterestDTO(**dict(zip(row.keys(), row)))
        return None

    async def update(self, interest_id: int, interest: InterestDTO) -> Optional[InterestDTO]:
        """
        Partial update of 'interests' row.
        Uses the DTO's filtered_dict() to skip empty/None fields.
        Returns the updated InterestDTO or None.
        """
        payload = interest.filtered_dict(exclude_none=True, exclude_empty_str=True)

        if not payload:
            existing = await self.get_by_id(interest_id)
            return existing

        set_clauses = [f"{key} = :{key}" for key in payload]
        set_clause_str = ", ".join(set_clauses)

        payload["id"] = interest_id

        query = text(f"""
            UPDATE interests
            SET {set_clause_str}
            WHERE id = :id
            RETURNING id, name
        """)

        result = await self._session.execute(query, payload)
        row = result.fetchone()
        if row:
            return InterestDTO(**dict(zip(row.keys(), row)))
        return None

    async def remove(self, interest_id: int) -> None:
        """
        Delete from 'interests' by ID.
        """
        query = text("DELETE FROM interests WHERE id = :id")
        await self._session.execute(query, {"id": interest_id})
        # No commit here either

    async def get_by_id(self, interest_id: int) -> Optional[InterestDTO]:
        """
        Fetch a single row by ID.
        """
        query = text("""
            SELECT id, name
            FROM interests
            WHERE id = :id
        """)
        result = await self._session.execute(query, {"id": interest_id})
        row = result.fetchone()
        if row:
            return InterestDTO(**dict(zip(row.keys(), row)))
        return None

    async def list(self, filters: Optional[Dict[str, Any]] = None) -> List[InterestDTO]:
        """
        Return a list of InterestDTO items, with optional filters.
        """
        base_query = "SELECT id, name FROM interests"
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
            InterestDTO(**dict(zip(row.keys(), row)))
            for row in rows
        ]
