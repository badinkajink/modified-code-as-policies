'''
This is a control API for a simple skid-steer robot leveraging Codex's code-generation. The API has access to to robotpy, a Python implementation of the FRC library, WPILib.

The robot-template module may further accommodate additional robot features, sensors, or mechanisms. Any such new features will be introduced with double # syntax. Example:
## The robot now has an RGB-D camera which reports image data in 1024x768  matrix form. Each entry represents a pixel with an (R,G,B,D) tuple.

Do not generate code that uses unmentioned features. As this is a code generated API, use the double # notation (##) to demarcate code that may not be reliable, feasible, or correct. For example, a user may request the following function:
# function that maintains bipedal gait 
## The skidsteer robot does not have limbs and cannot have bipedal gait. Ending code generation

Some functions may request feasible capabilities from features or hardware that have not been added to the robot. In these cases, ask for clarification and provide alternative options if possible. One such example:
# function that leverages accelerometer readings to execute trapezoidal motion profile in a specified direction
## The robot does not have an accelerometer, but this same function can be generated using readings from the wheel encoder and gyroscope. Proceed?

In all other situations which present uncertainty, lack of clarity, or potential lack of feasibility, use the ## syntax to request clarification, verification, or modification.
'''
import wpilib
from wpilib.drive import DifferentialDrive


class MyRobot(wpilib.TimedRobot):
    """This is a demo program showing how to use Gyro control with the
    DifferentialDrive class."""

    def robotInit(self):
        """Robot initialization function"""
        gyroChannel = 0  # analog input

        self.joystickChannel = 0  # usb number in DriverStation

        # channels for motors
        self.leftMotorChannel = 1
        self.rightMotorChannel = 0
        self.leftRearMotorChannel = 3
        self.rightRearMotorChannel = 2

        self.angleSetpoint = 0.0
        self.pGain = 1  # propotional turning constant

        # gyro calibration constant, may need to be adjusted
        # gyro value of 360 is set to correspond to one full revolution
        self.voltsPerDegreePerSecond = 0.0128

        self.left = wpilib.MotorControllerGroup(
            wpilib.Talon(self.leftMotorChannel), wpilib.Talon(self.leftRearMotorChannel)
        )
        self.right = wpilib.MotorControllerGroup(
            wpilib.Talon(self.rightMotorChannel),
            wpilib.Talon(self.rightRearMotorChannel),
        )
        self.myRobot = DifferentialDrive(self.left, self.right)

        self.gyro = wpilib.AnalogGyro(gyroChannel)
        self.joystick = wpilib.Joystick(self.joystickChannel)

    def teleopInit(self):
        """
        Runs at the beginning of the teleop period
        """
        self.gyro.setSensitivity(
            self.voltsPerDegreePerSecond
        )  # calibrates gyro values to equal degrees

    def teleopPeriodic(self):
        """
        Sets the gyro sensitivity and drives the robot when the joystick is pushed. The
        motor speed is set from the joystick while the RobotDrive turning value is assigned
        from the error between the setpoint and the gyro angle.
        """

        turningValue = (self.angleSetpoint - self.gyro.getAngle()) * self.pGain
        if self.joystick.getY() <= 0:
            # forwards
            self.myRobot.arcadeDrive(self.joystick.getY(), turningValue)
            self.rotateTo(30)
        elif self.joystick.getY() > 0:
            # backwards
            self.myRobot.arcadeDrive(self.joystick.getY(), -turningValue)

    # function to rotate robot to a specific degree and perform closed loop control on gyro heading feedback
    def rotateTo(self, degree):
        # print(f"hello {degree}")
        # set the angle setpoint to the degree provided by user
        self.angleSetpoint = degree

        # set sensitivity of gyro
        self.gyro.setSensitivity(self.voltsPerDegreePerSecond)

        # calculate error
        error = self.angleSetpoint - self.gyro.getAngle()

        # set a deadband for error
        if error <= 5:
            error = 0

        # rotate motors based on error and pGain
        self.myRobot.tankDrive(error * self.pGain, -error * self.pGain)


if __name__ == "__main__":
    wpilib.run(MyRobot)