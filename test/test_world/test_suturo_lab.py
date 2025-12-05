import pytest
from krrood.entity_query_language.entity import let, contains, entity
from krrood.entity_query_language.quantify_entity import an
from semantic_digital_twin.semantic_annotations.semantic_annotations import Floor, Room
from semantic_digital_twin.world import World
from semantic_digital_twin.datastructures.prefixed_name import PrefixedName
from semantic_digital_twin.world_description.world_entity import Body

from suturo_resources.suturo_map import load_environment, build_environment_walls, build_environment_furniture

def test_load_environment_returns_world():
    world = load_environment()
    assert isinstance(world, World)
    assert world.root.name == PrefixedName("root")

def test_kitchen_room():
    #world = World([Room(name=PrefixedName("kitchen"), floor=Floor(name=PrefixedName("floor1")))])
    world = load_environment()
    body = let(type_=Body, domain=world.bodies)
    query = an(entity(body, contains(body.name.name,"kitchen_room")))
    kitchen_room = list(query.evaluate())[0]
    kitchen_room : Floor
    print(kitchen_room)
    #query = an(entity(body, contains(body.name.name, "kitchen")))
    #print(*query.evaluate())

def test_living_room():
    #world = World([Room(name=PrefixedName("kitchen"), floor=Floor(name=PrefixedName("floor1")))])
    world = load_environment()
    body = let(type_=Body, domain=world.bodies)
    query = an(entity(body, contains(body.name.name,"living")))
    kitchen_room = list(query.evaluate())[0]
    kitchen_room : Floor
    print(kitchen_room)