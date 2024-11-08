import abc
from datetime import datetime , timezone
from typing import Dict, List, Mapping, Optional, Union

from pydantic import BaseConfig, BaseModel, Field
from serviceHandling.Eventhandling.events import get_db_client
from fastapi import  HTTPException, status
from bson.objectid import ObjectId
from core.config import log , settings
from serviceHandling.Schema.util import validate_object_id
from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase)

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class IDModelMixin(BaseModel):
    """
    Mixin to add ID field for schemas.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class UpdateDateTime(BaseModel):
    """
    Mixin to add updated timestamp for schemas.
    """
    updated_at: Optional[datetime] = Field(default_factory=datetime,alias="updated_at")


class CreateDateTime(BaseModel):
    """
    Mixin to add updated timestamp for schemas.
    """
    created_at: Optional[datetime] = Field(default_factory=datetime,alias="updated_at")


class DateTimeModelMixin(BaseModel):
    """
    Mixin to add create  timestamp for schemas.
    """
    
    updated_at: Optional[datetime] = Field(...,alias="updated_at")
    created_at: Optional[datetime] = Field(...,alias="create_at")
        
class BaseSchema(BaseModel):
    class Config(BaseConfig):
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        orm_mode = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt:  dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        }



class BaseRepository(abc.ABC):
    """Base repository for all database tables.

    Args:
        abc.ABC (Class): Abstract base class.
    """
    

    def __init__(self,db_client: AsyncIOMotorClient = get_db_client(), *args, **kwargs) -> None:
        self._db: AsyncIOMotorDatabase = db_client[settings.db_name]
        self._collection: AsyncIOMotorCollection = self._db[self._db_collection]
        super()

    @property
    @abc.abstractmethod
    def _db_collection(self):
        pass

    @property
    @abc.abstractmethod
    def _schema_create(self):
        pass

    @property
    @abc.abstractmethod
    def _schema_update(self):
        pass

    @property
    @abc.abstractmethod
    def _schema_out(self):
        pass

    def _preprocess_create(self, values: Union[BaseSchema, Dict]) -> Dict:
        if isinstance(values, dict):
            values = self._schema_create(**values)
        return dict(values)

    def _preprocess_update(self, values: Union[BaseSchema, Dict]) -> Dict:
        if isinstance(values, dict):
            values = self._schema_update(**values)
        return dict(values)

    async def _count_documents(self) -> int:
        return await self._collection.count_documents({})

    async def _get_object_or_404(self, id: str) -> Mapping:
        _id: ObjectId = validate_object_id(id)
        if (document := await self._collection.find_one({"_id": _id})) is not None:
            document["_id"] = str(id)
            return document
        log.warn(f"No Document with ObjectId { id } found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    async def _list(self, **kwargs) -> List[Mapping]:
        document_count: int = await self._count_documents()
        cursor = self._collection.find(kwargs)
        return await cursor.to_list(document_count)

    async def _paginated_list(self, limit: int, skip: int, **kwargs) -> List[Mapping]:
        document_count: int = await self._count_documents()
        cursor = self._collection.find(kwargs).limit(limit).skip(skip)
        return await cursor.to_list(document_count)

    async def _insert(self, values: dict):
        return await self._collection.insert_one(values)

    async def _update(self, id: str, values: dict):
        _id: ObjectId = validate_object_id(id)
        return await self._collection.update_one({"_id": _id}, {"$set": values})

    async def _delete_by_id(self, id: str):
        _id: ObjectId = validate_object_id(id)
        return await self._collection.delete_one({"_id": _id})

    async def count(self) -> int:
        """Fetch total count of objects in the collection.

        Returns:
            Document Count (int): Count of all document.
        """
        return await self._count_documents()

    async def fetch_by_id(self, id: str):
        """Fetch document object based on Object ID

        Args:
            id (str): Object ID as string.

        Returns:
            Result (dict): If object is found returns dictionary object.
        """
        return await self._get_object_or_404(id)

    async def fetch_by_attribute(self, attr: dict):
        """Fetch document object based on attributes

        Args:
            attr (dict): attr as a dict.

        Returns:
            Result (dict): If object is found returns dictionary object.
        """
        try:
            return await self._collection.find_one(attr)
        except Exception as err:
            log.warning(err)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Error while fetching oject by attribute")

    async def list(self, **kwargs):
        """Fetch list of documents based on limit if limit is 0 other wise based on limit and offset

        Returns:
            Documents (list): List of all found documents.
        """
        if "limit" in kwargs.keys() and kwargs["limit"] == 0:
            rows = await self._list()
        else:
            rows = await self._paginated_list(kwargs["limit"], kwargs["skip"], **kwargs)
        return [self._schema_out(**dict(row.items())) for row in rows]

    async def create(self, values: Union[BaseSchema, Dict]) -> BaseSchema:
        """Add new document object based on Payload

        Args:
            values (Union[BaseSchema, Dict]): Request Payload for create

        Raises:
            HTTPException: Error 400 if inserted Object ID is None

        Returns:
            BaseSchema: Returns newly added document Object.
        """
        dict_values = self._preprocess_create(values)
        new_document = await self._insert(dict_values)
        if new_document.inserted_id:
            return await self._get_object_or_404(new_document.inserted_id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error while creating new object")

    async def update(self, id: str, values: Union[BaseSchema, Dict]) -> BaseSchema:
        """Updates object based on Object ID and Payload.

        Args:
            id (str): [description]
            values (Union[BaseSchema, Dict]): Request Payload for update

        Raises:
            HTTPException: Error 400 if modified count is not 1

        Returns:
            Updated Object (BaseSchema): Returns updated object or existing if values dict.
        """
        existing_document = await self._get_object_or_404(id)
        dict_values = self._preprocess_update(values)
        values = {k: v for k, v in dict_values.items() if v is not None}

        if len(values) >= 1:
            update_document = await self._update(id, values)
            if update_document.modified_count == 1:
                if (updated_object := await self._get_object_or_404(id)) is not None:
                    return updated_object
        return existing_document

    async def delete(self, id: str):
        """Delete document object based on Object ID

        Args:
            id (str): Object ID as string

        Raises:
            HTTPException: Error 400 if deleted count is 0

        Returns:
            Response (dict): Success Message for Object delete operation.
        """
        await self._get_object_or_404(id)
        document = await self._delete_by_id(id)
        if document.deleted_count:
            return {"msg": f"Object { id } deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Error while deleting document id: { id }")


class Collections:
    invoice_collection = 'Invoices'
    user_collection = "users"
    activity_collection = "cache_activity"