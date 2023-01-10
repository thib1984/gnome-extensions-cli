import os
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, NoneStr  # pylint: disable=no-name-in-module


class Metadata(BaseModel):
    uuid: str
    name: str
    description: NoneStr
    extension_id: NoneStr = Field(alias="extension-id")
    shell_version: Optional[List[str]] = Field(alias="shell-version")
    url: NoneStr
    version: Optional[int]
    path: Optional[Path]


class _Version(BaseModel):
    pk: int
    version: int


class AvailableExtension(BaseModel):
    uuid: str
    pk: int
    name: str
    description: str
    creator: str
    creator_url: NoneStr
    link: NoneStr
    icon: NoneStr
    screenshot: NoneStr
    shell_version_map: Dict[str, _Version]
    version: Optional[int]
    version_tag: NoneStr
    download_url: NoneStr


@dataclass
class InstalledExtension:
    folder: Path

    @property
    def read_only(self):
        return not os.access(str(self.folder), os.W_OK)

    @cached_property
    def metadata(self) -> Metadata:
        return Metadata.parse_file(self.folder / "metadata.json")

    @property
    def uuid(self) -> str:
        return self.metadata.uuid