# Copyright (c) 2021 Boston Dynamics, Inc.  All rights reserved.
#
# Downloading, reproducing, distributing or otherwise using the SDK Software
# is subject to the terms and conditions of the Boston Dynamics Software
# Development Kit License (20191101-BDSDK-SL).

"""Tutorial to show how to use the Boston Dynamics API"""
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


def main(argv):
    username = 'user'
    password = 'hgprse58afaw'

    # Create robot object
    sdk = sdk.create_standard_sdk('uva-python-skeleton')
    robot = sdk.create_robot(username, password) # these can be replaced

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

            # Have the robot stand up
            robot.logger.info("Commanding robot to stand...")
            command_client = robot.ensure_client(RobotCommandClient.default_service_name)
            blocking_stand(command_client, timeout_sec=10)
            robot.logger.info("Robot standing.")
            time.sleep(3)

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
