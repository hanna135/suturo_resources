import logging
import os
from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple

from pycram.datastructures.dataclasses import Context
from semantic_digital_twin.adapters.urdf import URDFParser
from semantic_digital_twin.robots.hsrb import HSRB

from suturo_resources.suturo_map import load_environment

from semantic_digital_twin.datastructures.prefixed_name import PrefixedName
from semantic_digital_twin.spatial_types.spatial_types import HomogeneousTransformationMatrix
from semantic_digital_twin.world_description.world_entity import Body
from semantic_digital_twin.world_description.connections import FixedConnection, OmniDrive
from semantic_digital_twin.world_description.geometry import Box, Scale, Sphere
from semantic_digital_twin.world_description.shape_collection import ShapeCollection

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class WorldSetupPaths:
    hsrb_urdf: str
    milk_stl: str
    cereal_stl: str

def _here(*parts: str) -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *parts))

def default_paths() -> WorldSetupPaths:
    return WorldSetupPaths(
        hsrb_urdf=_here("..", "..", "resources", "robots", "hsrb.urdf"),
        milk_stl=_here("..", "..", "resources", "objects", "milk.stl"),
        cereal_stl=_here("..", "..", "resources", "objects", "breakfast_cereal.stl"),
    )

def build_hsrb_world(hsrb_urdf: str):
    world = URDFParser.from_file(file_path=hsrb_urdf).parse()
    with world.modify_world():
        odom = Body(name=PrefixedName("odom_combined"))
        world.add_kinematic_structure_entity(odom)
        world.add_connection(
            OmniDrive.create_with_dofs(parent=odom, child=world.root, world=world)
        )
    return world




def try_make_viz(world):
    try:
        import rclpy
        from semantic_digital_twin.adapters.viz_marker import VizMarkerPublisher

        node = rclpy.create_node("viz_marker")
        return VizMarkerPublisher(world, node)
    except Exception:
        logger.info(
            "VizMarkerPublisher is unavailable (ROS not running or deps missing)."
        )
        return None


def hsr_world_setup():
    hsr = ("/home/rody/SUTURO/Rody_cognitive_robot_abstract_machine/pycram/resources/robots/hsrb.urdf")
    hsr_parser = URDFParser.from_file(file_path=hsr)
    world_with_hsr = hsr_parser.parse()
    HSRB.from_world(world_with_hsr)
    with world_with_hsr.modify_world():
        hsr_root = world_with_hsr.root
        localization_body = Body(name=PrefixedName("odom_combined"))
        world_with_hsr.add_kinematic_structure_entity(localization_body)
        c_root_bf = OmniDrive.create_with_dofs(
            parent=localization_body, child=hsr_root, world=world_with_hsr
        )
        world_with_hsr.add_connection(c_root_bf)

    return world_with_hsr

def test_hsr_world_setup():
    world = hsr_world_setup()

def test_load_world():
    world = load_environment()
    all_elements_connections = world.connections
    root = world.root
    milk = Box(scale=Scale(0.10, 0.10, 0.20))
    shape_geometry = ShapeCollection([milk])
    milk_body = Body(name=PrefixedName("milk_body"), collision=shape_geometry, visual=shape_geometry)

    root_C_milk = FixedConnection(parent=root, child=milk_body,
                                  parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=3.545,
                                                                                                              y=0.626,
                                                                                                              z=0.9225))
    all_elements_connections.append(root_C_milk)

    apple = Sphere(radius=0.10)
    shape_geometry = ShapeCollection([apple])
    apple_body = Body(name=PrefixedName("apple_body"), collision=shape_geometry, visual=shape_geometry)

    root_C_apple = FixedConnection(parent=root, child=apple_body,
                                   parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=3.545,
                                                                                                               y=0.426,
                                                                                                               z=0.9225))
    all_elements_connections.append(root_C_apple)

    banana = Box(scale=Scale(0.20, 0.05, 0.05))
    shape_geometry = ShapeCollection([banana])
    banana_body = Body(name=PrefixedName("banana_body"), collision=shape_geometry, visual=shape_geometry)
    root_C_banana = FixedConnection(parent=root, child=banana_body,
                                    parent_T_connection_expression=HomogeneousTransformationMatrix.from_xyz_rpy(x=3.245,
                                                                                                                y=0.426,
                                                                                                                z=0.8225))
    all_elements_connections.append(root_C_banana)



    return world