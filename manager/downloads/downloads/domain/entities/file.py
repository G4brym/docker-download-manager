import hashlib
import json
import os
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Optional, Dict

from downloads.domain.settings import DOWNLOADS_PATH
from downloads.domain.value_objects import FailTypes


@dataclass(frozen=True)
class File:
    name: str
    path: str
    url: str
    retries: Optional[int] = 0
    creation_date: Optional[datetime] = None
    failed: Optional[FailTypes] = FailTypes.NoError
    completed: Optional[bool] = False
    completion_date: Optional[datetime] = None
    headers: Optional[Dict[str, str]] = None

    @property
    def file_path(self):
        return os.path.join(self.path, self.name)

    @property
    def abs_path(self):
        return os.path.join(DOWNLOADS_PATH, self.path)

    @property
    def hash(self):
        return self.__hash__()

    def __hash__(self):
        return hashlib.md5(self.file_path.encode("utf-8")).hexdigest()

    @classmethod
    def from_dict(cls, row: Dict) -> "File":
        if isinstance(row["headers"], str):
            row["headers"] = json.loads(row["headers"])

        return cls(
            name=row["name"],
            path=row["path"],
            url=row["url"],
            failed=FailTypes(row["failed"]),
            retries=row["retries"],
            creation_date=row["creation_date"],
            completed=row["completed"],
            completion_date=row["completion_date"],
            headers=row["headers"],
        )

    @classmethod
    def to_dict(cls, record: "File") -> Dict:
        return dict(
            hash=record.__hash__(),
            name=record.name,
            path=record.path,
            url=record.url,
            failed=record.failed.value,
            retries=record.retries,
            creation_date=record.creation_date,
            completed=record.completed,
            completion_date=record.completion_date,
            headers=record.headers,
        )

    def copy_with(self, **kwargs):
        return replace(self, **kwargs)
