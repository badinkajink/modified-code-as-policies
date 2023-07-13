#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#

import wpilib.simulation
from wpilib import RobotController
from pyfrc.physics.core import PhysicsInterface
from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units
from pyfrc.physics import drivetrains
from wpimath.system.plant import DCMotor
from wpimath.system import LinearSystemId

import typing

if typing.TYPE_CHECKING:
    from robot import MyRobot


class PhysicsEngine:
    """
    Simulates a motor moving something that strikes two limit switches,
    one on each end of the track. Obviously, this is not particularly
    realistic, but it's good enough to illustrate the point
    """

    def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):
        self.physics_controller = physics_controller

        # Motors
        self.l_motor = wpilib.simulation.PWMSim(robot.l_motor.getChannel())
        self.r_motor = wpilib.simulation.PWMSim(robot.r_motor.getChannel())

        # Wheel Encoders
        self.l_encoder = wpilib.simulation.EncoderSim(robot.l_encoder)
        self.r_encoder = wpilib.simulation.EncoderSim(robot.r_encoder)

        # Gyro
        self.gyro = wpilib.simulation.AnalogGyroSim(robot.gyro)

        # Accelerometer
        self.accelerometer = wpilib.simulation.BuiltInAccelerometerSim(robot.accelerometer)

        # Change these parameters to fit your robot!
        bumper_width = 3.25 * units.inch

        # unused
        self.dio1 = wpilib.simulation.DIOSim(robot.limit1)
        self.dio2 = wpilib.simulation.DIOSim(robot.limit2)
        self.ain2 = wpilib.simulation.AnalogInputSim(robot.position)
        self.motor = wpilib.simulation.PWMSim(robot.motor.getChannel())
        self.position = 0

        '''
        # Romi Motor Specs for reference: TI_RSLK MAX
        MOTOR_CFG_ROMI_MOTOR = MotorModelConfig(
            "Romi Motor",
            NOMINAL_VOLTAGE,
            150 * units.cpm,
            0.13 * units.amp,
            0.1765 * units.N_m,
            1.25 * units.amp,
        )
        # robot weight: 215g (0.47bs)
        # motors on 120:1 ratio
        # wheel diameter: 70mm (2.75")
        # trackwidth of 141mm (5.5")
        # 12cpr encoders, 1440 counts per revolution
        '''

        # fmt: off
        self.drivetrain = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_ROMI_MOTOR,           # motor configuration
            0.47 * units.lbs,                    # robot mass
            0.00833,                             # drivetrain gear ratio 120:1
            1,                                   # motors per side
            4 * units.inch,                     # robot wheelbase
            5.5 * units.inch,                   # robot width
            6 * units.inch,                     # robot length
            2.75 * units.inch,                  # wheel diameter
        )
        # fmt: on

        # https://github.com/robotpy/examples/blob/main/physics-camsim/src/physics.py
        self.system = LinearSystemId.identifyDrivetrainSystem(1.98, 0.2, 1.5, 0.3)
        # https://github.com/wpilibsuite/frc-docs/blob/main/source/docs/software/wpilib-tools/robot-simulation/drivesim-tutorial/drivetrain-model.rst
        self.drivesim = wpilib.simulation.DifferentialDrivetrainSim(
           J=0.215, gearing=0.008333, mass=0.215, wheelRadius=0.035, trackWidth=0.141, driveMotor=DCMotor.romiBuiltIn(1)
        )

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """

        # Simulate the drivetrain
        l_motor = self.l_motor.getSpeed()
        r_motor = self.r_motor.getSpeed()

        ###
        # EncoderSim
        l_speed = self.l_motor.getSpeed()
        r_speed = self.r_motor.getSpeed()

        voltage = RobotController.getInputVoltage()

        self.drivesim.setInputs(l_speed * voltage, r_speed * voltage)
        self.drivesim.update(tm_diff)

        self.l_encoder.setDistance(self.drivesim.getLeftPosition() * 39.37)
        self.l_encoder.setRate(self.drivesim.getLeftVelocity() * 39.37)
        self.r_encoder.setDistance(self.drivesim.getRightPosition() * 39.37)
        self.r_encoder.setRate(self.drivesim.getRightVelocity() * 39.37)
        ###

        transform = self.drivetrain.calculate(l_motor, r_motor, tm_diff)
        pose = self.physics_controller.move_robot(transform)

        # Update the gyro simulation
        # -> FRC gyros are positive clockwise, but the returned pose is positive
        #    counter-clockwise
        self.gyro.setAngle(-pose.rotation().degrees())

        # update position (use tm_diff so the rate is constant)
        self.position += self.motor.getSpeed() * tm_diff * 3

        # update limit switches based on position
        if self.position <= 0:
            switch1 = True
            switch2 = False

        elif self.position > 10:
            switch1 = False
            switch2 = True

        else:
            switch1 = False
            switch2 = False

        # set values here
        self.dio1.setValue(switch1)
        self.dio2.setValue(switch2)
        self.ain2.setVoltage(self.position)
