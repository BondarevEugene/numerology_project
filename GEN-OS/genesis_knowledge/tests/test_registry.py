from genesis_knowledge.registry.entity_factory import EntityFactory
from genesis_knowledge.registry.entity_registry import EntityRegistry
from genesis_knowledge.registry.enums import EntityType

factory = EntityFactory()
registry = EntityRegistry()
entity = factory.create(
    entity_type=EntityType.PROFESSION,
    title="Python Developer"
)
registry.add(entity)
print(registry.statistics())
print(registry.search("Python"))