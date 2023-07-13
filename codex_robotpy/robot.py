#!/usr/bin/env python3

import wpilib
import wpilib.drive

from robotpy_ext.autonomous import AutonomousModeSelector


class MyRobot(wpilib.TimedRobot):
    """
    This shows using the AutonomousModeSelector to automatically choose
    autonomous modes.

    If you find this useful, you may want to consider using the Magicbot
    framework, as it already has this integrated into it.
    """

    def robotInit(self):
        self.lstick = wpilib.Joystick(0)
        self.rstick = wpilib.Joystick(1)

        # Simple two wheel drive
        self.l_motor = wpilib.Talon(0)
        self.r_motor = wpilib.Talon(1)

        self.drive = wpilib.drive.DifferentialDrive(self.l_motor, self.r_motor)
        # Position gets automatically updated as robot moves
        self.gyro = wpilib.AnalogGyro(1)
        self.motor = wpilib.Talon(2)

        self.limit1 = wpilib.DigitalInput(1)
        self.limit2 = wpilib.DigitalInput(2)

        self.position = wpilib.AnalogInput(2)

        # Items in this dictionary are available in your autonomous mode
        # as attributes on your autonomous object
        self.components = {"drive": self.drive, "gyro": self.gyro, "motor": self.motor, 
                           "limit1": self.limit1, "limit2": self.limit2, "position": self.position }

        # * The first argument is the name of the package that your autonomous
        #   modes are located in
        # * The second argument is passed to each StatefulAutonomous when they
        #   start up
        self.automodes = AutonomousModeSelector("autonomous", self.components)

    def autonomousInit(self):
        self.drive.setSafetyEnabled(True)
        self.automodes.start()

    def autonomousPeriodic(self):
        self.automodes.periodic()

    def disabledInit(self):
        self.automodes.disable()

    def teleopPeriodic(self):
        """Called when operation control mode is enabled"""

        self.drive.arcadeDrive(self.lstick.getX(), self.lstick.getY())

        # Move a motor with a Joystick
        y = self.rstick.getY()

        # stop movement backwards when 1 is on
        if self.limit1.get():
            y = max(0, y)

        # stop movement forwards when 2 is on
        if self.limit2.get():
            y = min(0, y)

        self.motor.set(y)


if __name__ == "__main__":
    wpilib.run(MyRobot)
