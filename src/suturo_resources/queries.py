from typing import List

import numpy as np
#from semantic_digital_twin.world_description import *
from krrood.entity_query_language.entity import variable, entity, contains
from krrood.entity_query_language.entity_result_processors import an
from semantic_digital_twin import world
from semantic_digital_twin.collision_checking.trimesh_collision_detector import TrimeshCollisionDetector
from semantic_digital_twin.reasoning.predicates import Above, is_supported_by
from semantic_digital_twin.world import World
from semantic_digital_twin.world_description.world_entity import Region, Body, SemanticAnnotation
from semantic_digital_twin.spatial_types import HomogeneousTransformationMatrix
#from semantic_digital_twin.semantic_annotations.semantic_annotations import root_C_milk
from xacro import Table

from suturo_resources.suturo_map import load_environment


def query_region_area(world, region: str):
    """
    Queries the kitchen area from the environment.
    Returns the center of mass and global pose of the kitchen region.
    """
    body = variable(type_=Region, domain=world.regions)
    query = an(entity(body).where(contains(body.name.name, region)))
    kitchen_room_area = list(query.evaluate())[0]
    return kitchen_room_area



def query_trash(world):
    """
    Queries the location of the trash can in the environment.
    Returns the x, y, z coordinates of the trash can's global pose.
    """
    body = variable(type_=Body, domain=world.bodies)
    query = an(entity(body).where(contains(body.name.name, "trash_can_body")))
    trash_can = list(query.evaluate())[0]
    return trash_can



def bodies_above_body(main_body: Body) -> List[Body]:
    result= []
    bodies= []
    for connection in main_body._world.connections:
        if str(connection.parent.name) == "root":
            bodies.append(connection.child)
    for body in bodies:
        if body.combined_mesh == None:
            continue
        if is_supported_by(body, main_body, max_intersection_height=0.1):
            result.append(body)
    return result

def get_next_object(supporting_surface, pov):
    obj_distance = {}
    for obj in bodies_above_body(supporting_surface):
        dx = abs(obj.global_pose.x - pov[0])
        dy = abs(obj.global_pose.y - pov[1])
        dist_sq = dx + dy
        obj_distance[obj] = dist_sq
    sorted_objects = sorted(obj_distance.items(), key=lambda item: item[1])
    return sorted_objects