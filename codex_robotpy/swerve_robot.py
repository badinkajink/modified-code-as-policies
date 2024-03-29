#!/usr/bin/env python3

from ctre import WPI_TalonFX, CANifier
from ctre.sensors import WPI_CANCoder
import magicbot
import wpilib
from components.drivetrain import SwerveModule, SwerveChassis
from wpimath.geometry import Translation2d
from components.driverstation import FROGStick
from components.sensors import FROGGyro, FROGdar

# robot characteristics
# we are specifying inches and dividing by 12 to get feet,
# giving us values that can be used with the fromFeet method
# to get a correct Translation2d object
trackwidth = 27.75 / 12  # feet between wheels side to side
wheelbase = 21.75 / 12  # feet between wheels front to back

kDeadzone = 0.05


class FROGbot(magicbot.MagicRobot):
    """
    Initialize components here.
    """
    gyro: FROGGyro
    swerveChassis: SwerveChassis

    swerveFrontLeft: SwerveModule
    swerveFrontRight: SwerveModule
    swerveBackLeft: SwerveModule
    swerveBackRight: SwerveModule

    def createObjects(self):
        """Create motors and inputs"""
        # Swerve drive motors
        self.swerveFrontLeft_drive = WPI_TalonFX(11)
        self.swerveFrontRight_drive = WPI_TalonFX(12)
        self.swerveBackLeft_drive = WPI_TalonFX(13)
        self.swerveBackRight_drive = WPI_TalonFX(14)
        # Swerve steer motors
        self.swerveFrontLeft_steer = WPI_TalonFX(21)
        self.swerveFrontRight_steer = WPI_TalonFX(22)
        self.swerveBackLeft_steer = WPI_TalonFX(23)
        self.swerveBackRight_steer = WPI_TalonFX(24)
        # Swerve steer encoders (canifier)
        self.swerveFrontLeft_encoder = WPI_CANCoder(31)
        self.swerveFrontRight_encoder = WPI_CANCoder(32)
        self.swerveBackLeft_encoder = WPI_CANCoder(33)
        self.swerveBackRight_encoder = WPI_CANCoder(34)
        # Swerve module locations
        # TODO: move to swerveChassis?
        self.swerveFrontLeft_location = Translation2d.fromFeet(
            wheelbase / 2,
            trackwidth / 2,
        )
        self.swerveFrontRight_location = Translation2d.fromFeet(
            wheelbase / 2,
            -trackwidth / 2,
        )
        self.swerveBackLeft_location = Translation2d.fromFeet(
            -wheelbase / 2,
            trackwidth / 2,
        )
        self.swerveBackRight_location = Translation2d.fromFeet(
            -wheelbase / 2,
            -trackwidth / 2,
        )

        self.swerveFrontLeft_steerOffset = 0.0
        self.swerveFrontRight_steerOffset = 0.0
        self.swerveBackLeft_steerOffset = 0.0
        self.swerveBackRight_steerOffset = 0.0

        # config for saitek joystick
        self.driveStick = FROGStick(0, 0, 1, 3, 2)

    def teleopInit(self):
        """Called when teleop starts; optional"""
        self.swerveChassis.enable()
        pass

    def teleopPeriodic(self):
        """Called on each iteration of the control loop"""
        vX, vY, vT = (
            (self.driveStick.getFieldForward(), 0)[
                abs(self.driveStick.getFieldForward()) < kDeadzone
            ],
            (self.driveStick.getFieldLeft(), 0)[
                abs(self.driveStick.getFieldLeft()) < kDeadzone
            ],
            (self.driveStick.getFieldRotation(), 0)[
                abs(self.driveStick.getFieldRotation()) < kDeadzone
            ],
        )
        self.swerveChassis.field_oriented_drive(vX, vY, vT)

    def testInit(self):
        """Called when test mode starts; optional"""
        pass

    def testPeriodic(self):
        """Called on each iteration of the control loop"""
        pass


if __name__ == "__main__":
    wpilib.run(FROGbot)
