from typing import Optional, List, Dict, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user_image import UserImageDTO
from src.domain.repositories.iuser_image_repository import IUserImageRepository


class UserImageRepository(IUserImageRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, user_image: UserImageDTO) -> Optional[UserImageDTO]:
        """
        Insert a new record into 'user_images'.
        Returns the created UserImageDTO or None.
        """
        query = text("""
            INSERT INTO user_images (image_path, user_id)
            VALUES (:image_path, :user_id)
            RETURNING id, image_path, user_id
        """)

        # Use dict() or filtered_dict(), depending on whether you
        # want to skip None/empty. Typically for INSERT, we do full dict().
        params = user_image.dict()

        result = await self._session.execute(query, params)
        row = result.fetchone()
        # No commit here; rely on UoW

        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserImageDTO(**row_dict)
        return None

    async def update(self, user_image_id: int, user_image: UserImageDTO) -> Optional[UserImageDTO]:
        """
        Partially update 'user_images' by skipping fields that are None/empty
        via filtered_dict.
        """
        payload = user_image.filtered_dict(exclude_none=True, exclude_empty_str=True)

        # If nothing to update, return the existing record or None
        if not payload:
            existing = await self.get_by_id(user_image_id)
            return existing

        # Dynamically build the SET clause from the filtered payload
        set_clauses = [f"{col} = :{col}" for col in payload.keys()]
        set_clause_str = ", ".join(set_clauses)

        # Include the ID in the payload for the WHERE clause
        payload["id"] = user_image_id

        query = text(f"""
            UPDATE user_images
            SET {set_clause_str}
            WHERE id = :id
            RETURNING id, image_path, user_id
        """)

        result = await self._session.execute(query, payload)
        row = result.fetchone()
        # No commit here; rely on UoW

        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserImageDTO(**row_dict)
        return None

    async def remove(self, user_image_id: int) -> None:
        """
        Delete from 'user_images' by ID.
        """
        query = text("DELETE FROM user_images WHERE id = :id")
        await self._session.execute(query, {"id": user_image_id})
        # No commit here; rely on UoW

    async def get_by_id(self, user_image_id: int) -> Optional[UserImageDTO]:
        """
        Fetch a single user_images row by ID.
        """
        query = text("""
            SELECT id, image_path, user_id
            FROM user_images
            WHERE id = :id
        """)
        result = await self._session.execute(query, {"id": user_image_id})
        row = result.fetchone()
        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserImageDTO(**row_dict)
        return None

    async def get_by_user_id(self, user_id: int) -> Optional[UserImageDTO]:
        """
        Fetch the first user_images row matching a user_id.
        If you may have multiple images per user, change this
        to return a list. For now, we return just one or None.
        """
        query = text("""
            SELECT id, image_path, user_id
            FROM user_images
            WHERE user_id = :user_id
            LIMIT 1
        """)
        result = await self._session.execute(query, {"user_id": user_id})
        row = result.fetchone()
        if row:
            row_dict = dict(zip(row.keys(), row))
            return UserImageDTO(**row_dict)
        return None

    async def list(self, filters: Optional[Dict[str, Any]] = None) -> List[UserImageDTO]:
        """
        Return a list of UserImageDTOs with optional filtering.
        """
        base_query = "SELECT id, image_path, user_id FROM user_images"

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
            UserImageDTO(**dict(zip(row.keys(), row)))
            for row in rows
        ]
