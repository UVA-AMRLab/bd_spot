"""
Author: Shijie Gao, Jacob Higgins
Copyright: Copyright 2021, UVA AMR Spot
Version: 1.0.2
Date: Apr. 15 2021
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
from bosdyn.client import create_standard_sdk
from bosdyn.client.lease import LeaseClient, LeaseKeepAlive

import curses
import pdb

def main():
    username = 'user'
    password = 'hgprse58afaw'
    hostname = '192.168.80.3'

    # Create robot object
    sdk = create_standard_sdk('uva-python-skeleton')
    robot = sdk.create_robot(hostname) # these can be replaced
    id_client = robot.ensure_client('robot-id')
    id_client.get_id() 

    # Authenticate the robot
    robot.authenticate(username, password)

    # Acquire Lease
    lease_client = robot.ensure_client(bosdyn.client.lease.LeaseClient.default_service_name)
    lease = lease_client.acquire()
    lease_keepalive = LeaseKeepAlive(lease_client)

    # Create estop client for the robot
    estop_client = robot.ensure_client(bosdyn.client.estop.EstopClient.default_service_name)
    estop_endpoint = bosdyn.client.estop.EstopEndpoint(client=estop_client, name='skeleton_estop', estop_timeout=9.0)
    estop_endpoint.force_simple_setup()
    estop_keep_alive = bosdyn.client.estop.EstopKeepAlive(estop_endpoint)

    pdb.set_trace()

    robot.logger.info("E-stop created and realeased.")
    estop_keep_alive.allow()

    robot.time_sync.wait_for_sync()

    robot.logger.info("Powering on robot.")
    robot.power_on(timeout_sec=10)

    assert robot.is_powered_on(), "Robot power on failed."
    robot.logger.info("Robot powered on.")

    robot.logger.info("E-stop released.")
    estop_keep_alive.allow()

    # Have the robot stand up
    robot.logger.info("Commanding robot to stand...")
    command_client = robot.ensure_client(RobotCommandClient.default_service_name)
    blocking_stand(command_client, timeout_sec=10)
    robot.logger.info("Robot standing.")
    time.sleep(1)

    pdb.set_trace()
    stdscr = curses.initscr()
    try:
            with bosdyn.client.lease.LeaseKeepAlive(lease_client):
                while True:
                    c = stdscr.getch()
                    if c == ord(' '):
                        estop_keep_alive.settle_then_cut()        
                    else:
                        pass
                        # HERE GOES THE WONDERFUL CODES

            # Power the robot off. By specifying "cut_immediately=False", a safe power off command
            # is issued to the robot. This will attempt to sit the robot before powering off.     
            robot.power_off(cut_immediately=False, timeout_sec=20)
            assert not robot.is_powered_on(), "Robot power off failed."
            robot.logger.info("Robot safely powered off.")
    finally:
        # If we successfully acquired a lease, return it.
        lease_client.return_lease(lease)

if __name__ == '__main__':
    main()
