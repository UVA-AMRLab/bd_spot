"""
Author: Shijie Gao
Copyright: Copyright 2021, UVA AMR Spot
Version: 1.1.1
Date: Apr. 12 2021
Status: under developing
"""
from __future__ import print_function
# import sys
# import time
# import os
import bosdyn.client
from bosdyn.client.estop import EstopClient, EstopEndpoint, EstopKeepAlive
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive

import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.geometry

from bosdyn.client.image import ImageClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand

import curses

# LOGGER = logging.getLogger() # not sure how this works


class spot(username, password)

    def __init__(self, username, password):
        self._sdk = sdk.create_standard_sdk('uva-python-skeleton')
        self._robot = self._sdk.create_robot(username, password)

        # Create estop client for the robot
        self._estop_client = self._robot.ensure_client(EstopClient.default_service_name)
        self._estop_endpoint = EstopEndpoint(client=self._estop_client, name='skeleton_estop', estop_timeout=9.0)
        self._estop_endpoint.force_simple_setup()
        self._estop_keep_alive = EstopKeepAlive(self._estop_endpoint)

        # # logging
        # self._robot.logger.info("E-stop created and triggered.")
        self._estop_keep_alive.stop()

        # Authenticate the robot
        try:
            self._robot.authenticate(username, password)
            # self._robot.start_time_sync(options.time_sync_interval_sec)
        except RpcError as err:
            LOGGER.error("Failed to communicate with robot: %s" % err)
            return False
        
        # Acquire Lease
        self._lease_client = robot.ensure_client(LeaseClient.default_service_name)
        self._lease = self._lease_client.acquire()

    # Methods
    # bring up the robot (auth, estop, lease)
    def start(self):
        self._lease_keepalive = LeaseKeepAlive(self._lease_client)
    # stand up with default height
    def stand(height=1.0):
        pass
    # move the robot
    def move(angular, linear):
        pass

    def function():
        pass

    def estop:
        pass




def main(argv):
    username = 'user'
    password = 'hgprse58afaw'

    robot = spot(username, password)
    robot.start()

    try:
        with LeaseKeepAlive(robot._lease_client)

            while robot._estop_client.get_status(): # condition not done
                # major logic got here


            # Power the robot off
            robot._robot.power_off(cut_immediately=False, timeout_sec=20)
            assert not robot._robot.is_powered_on(), "Robot power off failed."
            # robot.logger.info("Robot safely powered off.")
    finally:
        # Return lease when finish
        lease_client.return_lease(lease)


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)
