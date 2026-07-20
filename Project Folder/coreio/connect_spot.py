from __future__ import annotations

import logging 
import os
import bosdyn.client
from bosdyn.client.robot import Robot
from bosdyn.client.robot_state import RobotStateClient

from .authentication import authenticate_robot, load_credentials

LOGGER=logging.getLogger(__name__)

class SpotConnection:
    def __init__(self)->None:
        self.robot_ip = os.getenv("SPOT_ROBOT_IP","").strip()
        if not self.robot_ip:
            raise RuntimeError("SPOT_ROBOT_IP is not configured")
        self.sdk = bosdyn.client.create_standard_sdk("spot-door-inspection")
        self.robot: Robot | None = None
    
    def connect(self)->Robot:
        LOGGER.info("Creating Spot SDK connection...")
        robot = self.sdk.create_robot(self.robot_ip)
        credentials = load_credentials()
        authenticate_robot(robot, credentials)
        LOGGER.info("Authentication completed!")

        robot.time_sync.wait_for_sync(timeout_sec = 30)
        LOGGER.info("Time sync complete!")
        self.robot = robot
        return robot
    
    def verify_read_only_connection(self) -> dict:
        """
        Verify authentication without commanding motion.
        This only requests robot state.
        """
        if self.robot is None:
            self.connect()
            
        state_client = self.robot.ensure_client(
            RobotStateClient.default_service_name
        )
        state = state_client.get_robot_state()
        
        return {
            "authenticated": True,
            "serial_number": (
                state.kinematic_state.transforms_snapshot.child_to_parent_edge_map
                is not None
            ),
            "battery_count": len(state.battery_states),
            "motor_power_state": state.power_state.motor_power_state,
        }

    def shutdown(self) -> None:
        if self.robot is not None:
            self.robot.stop_time_sync()
            self.robot.shutdown()
            self.robot = None

