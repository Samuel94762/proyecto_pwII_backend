from typing import Any, Dict, Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar("T")


class ResponseObject(BaseModel, Generic[T]):
    data: T
    msg: str


class ResponseList(BaseModel, Generic[T]):
    data: List[T]
    msg: str


class ResponseTotal(BaseModel, Generic[T]):
    msg: str
    total: int
    data: List[T]


class ResponseDictList(BaseModel):
    msg: str
    total: int
    data: Dict[str, List[Any]]