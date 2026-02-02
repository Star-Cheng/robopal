import os

import numpy as np

from robopal.robots.base import BaseRobot

ASSET_DIR = os.path.join(os.path.dirname(__file__), '../assets')

class Piper(BaseRobot):
    """ Piper robot base class. """
    def __init__(self,
                scene='default',
                manipulator='piper',
                gripper=None,
                mount=None
                ):
        super().__init__(
            scene=scene,
            mount=mount,
            manipulator=manipulator,
            gripper=gripper,
            attached_body='0_attachment',
        )
        self.arm_joint_names = {self.agents[0]: ['0_joint1', '0_joint2', '0_joint3', '0_joint4', '0_joint5', '0_joint6']}
        self.arm_actuator_names = {self.agents[0]: ['0_0_joint1', '0_0_joint2', '0_0_joint3', '0_0_joint4', '0_0_joint5', '0_0_joint6']}
        self.base_link_name = {self.agents[0]: '0_base_link'}
        self.end_name = {self.agents[0]: '0_attachment'}

        self.pos_max_bound = np.array([0.6, 0.6, 0.4])
        self.pos_min_bound = np.array([0.1, -0.6, -0.15])

    @property
    def init_qpos(self):
        """ Robot's init joint position. """
        return {self.agents[0]: np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])}

class PiperGrasp(Piper):
    def __init__(self):
        super().__init__(scene='grasping',
                         gripper='PiPERGripper',
                         mount='top_point')

        self.end_name = {self.agents[0]: '0_eef'}

    def add_assets(self):
        self.mjcf_generator.add_node_from_xml(ASSET_DIR + '/objects/cube/green_cube.xml')

    @property
    def init_qpos(self):
        """ Robot's init joint position. """
        return {self.agents[0]: np.array([0.0/57.2958, 90.0/57.2958, -80.0/57.2958, 0.0/57.2958, 65.0/57.2958, 0.0/57.2958])}
        # return {self.agents[0]: np.array([0.0/57.2958, 0.0/57.2958, 0.0/57.2958, 0.0/57.2958, .0/57.2958, 0.0/57.2958])}

class PiperPickAndPlace(PiperGrasp):

    def add_assets(self):
        super().add_assets()
        goal_site = """<site name="goal_site" pos="0.4 0.0 0.5" size="0.02 0.02 0.02" rgba="1 0 0 1" type="sphere" />"""
        self.mjcf_generator.add_node_from_str('worldbody', goal_site)

