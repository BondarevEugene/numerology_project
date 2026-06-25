from .base_entity import BaseEntity


class Behavior(BaseEntity):

    def __init__(self,id,title):

        super().__init__(
            id=id,
            title=title,
            entity_type="behavior"
        )