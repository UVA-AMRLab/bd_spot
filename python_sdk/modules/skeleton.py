"""
Author: Shijie Gao
Copyright: Copyright 2021, UVA AMR Spot
Version: 1.0.1
Date: Apr. 12 2021
Status: under developing
"""
from __future__ import print_function
import sys
import time
import os
import bosdyn.client
import bosdyn.client.lease
import bosdyn.client.util
import bosdyn.geometry

from bosdyn.client.image import ImageClient
from bosdyn.client.robot_command import RobotCommandBuilder, RobotCommandClient, blocking_stand

import curses

def main(argv):
    username = 'user'
    password = 'hgprse58afaw'

    # Create robot object
    sdk = sdk.create_standard_sdk('uva-python-skeleton')
    robot = sdk.create_robot(username, password) # these can be replaced

    # Initialize curses screen display
    stdscr = curses.initscr()

    # Create estop client for the robot
    estop_client = robot.ensure_client(bosdyn.client.estop.EstopClient.default_service_name)
    estop_endpoint = bosdyn.client.estop.EstopEndpoint(client=estop_client, name='skeleton_estop', estop_timeout=9.0)
    estop_endpoint.force_simple_setup()
    estop_keep_alive = bosdyn.client.estop.EstopKeepAlive(estop_endpoint)
    robot.logger.info("E-stop created and triggered.")
    estop_keep_alive.stop()

    # Authenticate the robot
    try:
        robot.authenticate(options.username, options.password)
        robot.start_time_sync(options.time_sync_interval_sec)
    except RpcError as err:
        LOGGER.error("Failed to communicate with robot: %s" % err)
        return False
    
    # Acquire Lease
    lease_client = robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)
    lease = lease_client.acquire()
    

    try:
        with bosdyn.client.lease.LeaseKeepAlive(lease_client):
            robot.logger.info("Powering on robot.")
            robot.power_on(timeout_sec=20)
            assert robot.is_powered_on(), "Robot power on failed."
            robot.logger.info("Robot powered on.")

            robot.logger.info("E-stop released.")
            estop_keep_alive.allow()

            # Have the robot stand up
            robot.logger.info("Commanding robot to stand...")
            command_client = robot.ensure_client(RobotCommandClient.default_service_name)
            blocking_stand(command_client, timeout_sec=10)
            robot.logger.info("Robot standing.")
            time.sleep(3)

            while True:
                c = stdscr.getch()
                if c == ord(' '):
                    estop_keep_alive.stop()
                    break
                else
                    #
                    # Algorithms goes here
                    #

            # Power the robot off
            robot.power_off(cut_immediately=False, timeout_sec=20)
            assert not robot.is_powered_on(), "Robot power off failed."
            robot.logger.info("Robot safely powered off.")
    finally:
        # Return lease when finish
        lease_client.return_lease(lease)


if __name__ == '__main__':
    if not main(sys.argv[1:]):
        sys.exit(1)
