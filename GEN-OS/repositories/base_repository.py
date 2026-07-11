"""
===============================================================================

 GENESIS HR®
 GEN-OS FILE
 ----
 repositories/base_repository.py

 BUILD ----- 0.2.1
 DESCRIPTION
 -----------
 Generic in-memory repository.
 Every domain repository inherits
 from this class.
===============================================================================
"""

from __future__ import annotations

from typing import Dict
from typing import Generic
from typing import Iterator
from typing import Optional
from typing import TypeVar

import logging


LOGGER = logging.getLogger(
    "GEN-OS.Repository"
)

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Generic repository.
    Stores domain objects indexed by id.
    """

    def __init__(self):
        self._items: Dict[str, T] = {}

    # ------------------------------------------------------------

    def add(
        self,
        item: T
    ) -> T:

        self._items[item.id] = item
        return item

    # ------------------------------------------------------------

    def add_many(
        self,
        items
    ):

        for item in items:

            self.add(item)

    # ------------------------------------------------------------

    def get(
        self,
        object_id: str
    ) -> Optional[T]:

        return self._items.get(
            object_id
        )

    # ------------------------------------------------------------

    def exists(
        self,
        object_id: str
    ) -> bool:

        return object_id in self._items

    # ------------------------------------------------------------

    def all(self):

        return list(
            self._items.values()
        )

    # ------------------------------------------------------------

    def remove(
        self,
        object_id: str
    ) -> bool:

        if object_id not in self._items:

            return False

        del self._items[
            object_id
        ]

        return True

    # ------------------------------------------------------------

    def clear(self):

        self._items.clear()

    # ------------------------------------------------------------

    def count(self):

        return len(
            self._items
        )
    # ------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------

    def first(self) -> Optional[T]:
        """
        Return first object.
        """

        return next(
            iter(self._items.values()),
            None
        )

    # ------------------------------------------------------------

    def last(self) -> Optional[T]:
        """
        Return last object.
        """

        if not self._items:

            return None

        return list(
            self._items.values()
        )[-1]

    # ------------------------------------------------------------

    def find_by_name(
        self,
        name: str
    ) -> Optional[T]:
        """
        Exact name search.
        """

        name = name.lower().strip()

        for item in self._items.values():

            item_name = getattr(
                item,
                "name",
                ""
            ).lower()

            if item_name == name:

                return item

        return None

    # ------------------------------------------------------------

    def search(
        self,
        text: str
    ) -> list[T]:
        """
        Full text search.
        """

        text = text.lower()

        result = []

        for item in self._items.values():

            name = getattr(
                item,
                "name",
                ""
            )

            description = getattr(
                item,
                "description",
                ""
            )

            title = getattr(
                item,
                "title",
                ""
            )

            haystack = (

                f"{name} "

                f"{title} "

                f"{description}"

            ).lower()

            if text in haystack:

                result.append(item)

        return result

    # ------------------------------------------------------------

    def filter(
        self,
        predicate
    ) -> list[T]:
        """
        Generic filtering.
        """

        return [

            item

            for item in self._items.values()

            if predicate(item)

        ]

    # ------------------------------------------------------------

    def sorted(
        self,
        key=None,
        reverse=False
    ) -> list[T]:
        """
        Sorted repository.
        """

        if key is None:

            key = lambda x: getattr(
                x,
                "name",
                ""
            )

        return sorted(

            self._items.values(),

            key=key,

            reverse=reverse

        )

    # ------------------------------------------------------------

    def random(self) -> Optional[T]:
        """
        Random object.
        """

        import random

        if not self._items:

            return None

        return random.choice(

            self.all()

        )

    # ------------------------------------------------------------

    def statistics(self) -> dict:
        """
        Repository statistics.
        """

        enabled = 0

        disabled = 0

        for item in self._items.values():

            if getattr(
                item,
                "enabled",
                True
            ):

                enabled += 1

            else:

                disabled += 1

        return {

            "objects":
                self.count(),

            "enabled":
                enabled,

            "disabled":
                disabled

        }

    # ------------------------------------------------------------

    def names(self) -> list[str]:
        """
        Return object names.
        """

        return [

            getattr(
                item,
                "name",
                ""
            )

            for item in self._items.values()

        ]
    # ------------------------------------------------------------
    # INDEXES
    # ------------------------------------------------------------

    def tags(self) -> dict[str, list[T]]:
        """
        Build tag index.
        """

        index: dict[str, list[T]] = {}

        for item in self._items.values():

            for tag in getattr(item, "tags", []):

                index.setdefault(
                    tag,
                    []
                ).append(item)

        return index

    # ------------------------------------------------------------

    def find_by_tag(
        self,
        tag: str
    ) -> list[T]:
        """
        Find objects by tag.
        """

        tag = tag.lower()

        return [

            item

            for item in self._items.values()

            if tag in [

                t.lower()

                for t in getattr(
                    item,
                    "tags",
                    []
                )

            ]

        ]

    # ------------------------------------------------------------

    def metadata_search(
        self,
        key: str,
        value
    ) -> list[T]:
        """
        Search metadata.
        """

        result = []

        for item in self._items.values():

            metadata = getattr(
                item,
                "metadata",
                {}
            )

            if metadata.get(key) == value:

                result.append(item)

        return result

    # ------------------------------------------------------------
    # EXPORT
    # ------------------------------------------------------------

    def to_dict(self) -> list[dict]:
        """
        Export repository.
        """

        result = []

        for item in self._items.values():

            if hasattr(item, "to_dict"):

                result.append(
                    item.to_dict()
                )

            else:

                result.append(
                    vars(item)
                )

        return result

    # ------------------------------------------------------------

    def ids(self) -> list[str]:

        return list(
            self._items.keys()
        )

    # ------------------------------------------------------------

    def values(self):

        return self._items.values()

    # ------------------------------------------------------------

    def items(self):

        return self._items.items()

    # ------------------------------------------------------------

    def __contains__(
        self,
        object_id: str
    ):

        return object_id in self._items

    # ------------------------------------------------------------

    def __getitem__(
        self,
        object_id: str
    ) -> T:

        return self._items[
            object_id
        ]

    # ------------------------------------------------------------

    def __iter__(self):

        return iter(
            self._items.values()
        )

    # ------------------------------------------------------------

    def __len__(self):

        return len(
            self._items
        )

    # ------------------------------------------------------------

    def __repr__(self):

        return (

            f"<{self.__class__.__name__} "

            f"count={self.count()}>"

        )