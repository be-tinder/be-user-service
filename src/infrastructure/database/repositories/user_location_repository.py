from typing import Optional, List, Dict, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user_location import UserLocationDTO
from src.domain.repositories.iuser_location_repository import IUserLocationRepository


class UserLocationRepository(IUserLocationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, user_location: UserLocationDTO) -> Optional[UserLocationDTO]:
        """
        Insert a new record into 'user_locations'.
        Returns the created UserLocationDTO or None.
        """
        query = text("""
            INSERT INTO user_locations (
                latitude, 
                longitude, 
                user_id
            )
            VALUES (
                :latitude, 
                :longitude, 
                :user_id
            )
            RETURNING 
                id,
                latitude,
                longitude,
                user_id
        """)

        # Use dict() or filtered_dict() as needed.
        # Typically for add, we do dict().
        params = user_location.dict()

        result = await self._session.execute(query, params)
        row = result.fetchone()
        # No commit, rely on UoW.

        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserLocationDTO(**row_dict)
        return None

    async def update(self, location_id: int, user_location: UserLocationDTO) -> Optional[UserLocationDTO]:
        """
        Partially update 'user_locations' by skipping None or empty fields
        (assuming filtered_dict does that).
        """
        payload = user_location.filtered_dict(exclude_none=True, exclude_empty_str=True)

        if not payload:
            # If there's nothing to update, return the existing record
            existing = await self.get_by_id(location_id)
            return existing

        # Build dynamic SET clause
        set_clauses = [f"{key} = :{key}" for key in payload.keys()]
        set_clause_str = ", ".join(set_clauses)

        payload["id"] = location_id

        query = text(f"""
            UPDATE user_locations
            SET {set_clause_str}
            WHERE id = :id
            RETURNING
                id,
                latitude,
                longitude,
                user_id
        """)

        result = await self._session.execute(query, payload)
        row = result.fetchone()
        # No commit, rely on UoW.

        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserLocationDTO(**row_dict)
        return None

    async def remove(self, location_id: int) -> None:
        """
        Delete a user location by ID from 'user_locations'.
        """
        query = text("DELETE FROM user_locations WHERE id = :id")
        await self._session.execute(query, {"id": location_id})
        # No commit, rely on UoW.

    async def get_by_id(self, location_id: int) -> Optional[UserLocationDTO]:
        """
        Fetch a single user location by its primary key (id).
        """
        query = text("""
            SELECT
                id,
                latitude,
                longitude,
                user_id
            FROM user_locations
            WHERE id = :id
        """)
        result = await self._session.execute(query, {"id": location_id})
        row = result.fetchone()
        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserLocationDTO(**row_dict)
        return None

    async def get_by_user_id(self, user_id: int) -> Optional[UserLocationDTO]:
        """
        Fetch a user location row by the user's ID.
        If there's only one row per user, return it or None.
        If multiple rows per user can exist, consider returning a list.
        """
        query = text("""
            SELECT
                id,
                latitude,
                longitude,
                user_id
            FROM user_locations
            WHERE user_id = :user_id
            LIMIT 1
        """)
        result = await self._session.execute(query, {"user_id": user_id})
        row = result.fetchone()
        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserLocationDTO(**row_dict)
        return None

    async def list(self, filters: Optional[Dict[str, Any]] = None) -> List[UserLocationDTO]:
        """
        Return a list of UserLocationDTO objects, with optional filtering.
        """
        base_query = """
            SELECT
                id,
                latitude,
                longitude,
                user_id
            FROM user_locations
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
            UserLocationDTO(**dict(zip(row.keys(), row)))
            for row in rows
        ]
