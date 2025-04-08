from typing import List, Optional, Dict, Any
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.data_collection import DataCollection
from app.schemas.data_collection import DataCollectionCreate, DataCollectionUpdate

class CRUDDataCollection(CRUDBase[DataCollection, DataCollectionCreate, DataCollectionUpdate]):
    """CRUD operations for DataCollection"""
    
    async def get_by_id(self, db: AsyncSession, dataid: str) -> Optional[DataCollection]:
        """Get data collection by ID"""
        result = await db.execute(select(DataCollection).where(DataCollection.dataid == dataid))
        return result.scalars().first()
    
    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[DataCollection]:
        """Get multiple data collections with pagination"""
        result = await db.execute(
            select(DataCollection).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    async def search(
        self, db: AsyncSession, *, keyword: str, skip: int = 0, limit: int = 100
    ) -> List[DataCollection]:
        """Search data collections by title or description"""
        result = await db.execute(
            select(DataCollection)
            .where(
                or_(
                    DataCollection.title.ilike(f"%{keyword}%"),
                    DataCollection.description.ilike(f"%{keyword}%")
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def create(
        self, db: AsyncSession, *, obj_in: DataCollectionCreate
    ) -> DataCollection:
        """Create new data collection"""
        db_obj = DataCollection(
            dataid=str(uuid4()),
            title=obj_in.title,
            description=obj_in.description,
            data=obj_in.data
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: DataCollection,
        obj_in: DataCollectionUpdate
    ) -> DataCollection:
        """Update data collection"""
        update_data = obj_in.dict(exclude_unset=True)
        
        # Update only provided fields
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def remove(self, db: AsyncSession, *, dataid: str) -> Optional[DataCollection]:
        """Remove data collection"""
        db_obj = await self.get_by_id(db, dataid=dataid)
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj
    
    async def clear_all(self, db: AsyncSession) -> int:
        """Clear all data collections"""
        result = await db.execute(select(DataCollection))
        all_data = result.scalars().all()
        count = len(all_data)
        
        for item in all_data:
            await db.delete(item)
        
        await db.commit()
        return count

# Create CRUD instance
data_collection = CRUDDataCollection(DataCollection)