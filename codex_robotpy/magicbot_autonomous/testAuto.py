from logging import Logger

from components.drivetrain import SwerveChassis
from magicbot import AutonomousStateMachine, state, timed_state
from wpimath.geometry import Transform2d, Pose2d, Rotation2d
from wpimath.units import degreesToRadians, inchesToMeters, feetToMeters
from pathplannerlib import PathPoint


class NoAuto(AutonomousStateMachine):
    MODE_NAME = "No Auto (default)"

    @state(first=True)
    def doNothing(self):
        pass

class moveForward(AutonomousStateMachine):
    MODE_NAME = "Move Forward"
    DEFAULT = True
    swerveChassis: SwerveChassis
    startX = 2.47
    endX = 1.81

    @state(first=True)
    def doNothing(self):
        self.next_state('moveForward')

    @timed_state(duration=2)
    def moveForward(self, initial_call):
        self.swerveChassis.field_oriented_drive(0.150, 0, 0)

    @state()
    def end(self):
        self.done()

class driveFiveFeet(AutonomousStateMachine):
    MODE_NAME = "Drive Five Feet"
    
    swerveChassis: SwerveChassis
    startX = 2.47
    endX = 1.81

    @state(first=True)
    def doNothing(self, initial_call):
        self.next_state('driveFiveFeet')

    @timed_state(duration=4)
    def driveFiveFeet(self, initial_call):
        if initial_call:
            self.swerveChassis.initializeChassisControllers()
            self.swerveChassis.setClosedLoopController(self.swerveChassis.holonomicController)
            self.swerveChassis.holonomicController.path = [
                PathPoint(self.swerveChassis.getRobotX() + 0.5,
                self.swerveChassis.getRobotY(), self.swerveChassis.getRobotHeading()),
                PathPoint(self.swerveChassis.getRobotX() + 6,
                self.swerveChassis.getRobotY(), self.swerveChassis.getRobotHeading())]
            self.swerveChassis.holonomicController.startClosedLoop()
        self.swerveChassis.autoDrive()
        if self.swerveChassis.holonomicController.atReference():
            self.swerveChassis.holonomicController.stopClosedLoop()
            self.swerveChassis.enableChassisPID()


# class moveForward(AutonomousStateMachine):
#     MODE_NAME = "Place cone, drive forward"

#     swerveChassis: SwerveChassis
#     startX = 2.47
#     endX = 1.81

#     @state(first=True)
#     def raiseArm(self, initial_call):
#         if initial_call:
#             self.armControl.next_state('moveToUpper')
#         self.armControl.engage()
#         if self.armControl.last_state == 'atUpper':
#             self.next_state('moveBack')

#     @timed_state(duration=2, next_state='dropCone')
#     def moveBack(self, initial_call):
#         self.swerveChassis.fieldOrientedDrive(-0.125, 0, 0)
#         # self.swerveChassis.autoDrive()
#         # if self.swerveChassis.holonomicController.atReference():
#         #     self.next_state("dropCone")

#     @state()
#     def dropCone(self, initial_call):
#         if initial_call:
#             self.grabberControl.next_state('dropping')
#         self.grabberControl.engage()
#         if not self.grabberControl.hasObject:
#             self.next_state('moveForward')


#     @timed_state(duration=4, next_state='dropArm')
#     def moveForward(self, initial_call):
#         self.swerveChassis.fieldOrientedDrive(0.150, 0, 0)
        
#     @state()
#     def dropArm(self, initial_call):
#         if initial_call:
#             self.swerveChassis.fieldOrientedDrive(0, 0, 0)
#             self.armControl.next_state('moveToHome')
#         self.armControl.engage()
#         if self.armControl.last_state == 'atHome':
#             self.next_state('end')

#     @state()
#     def end(self):
#         self.done()


# class placeConeDriveToCharge(AutonomousStateMachine):
#     MODE_NAME = "Place cone, drive to Charging"

#     swerveChassis: SwerveChassis
#     armControl: ArmControl
#     grabberControl: GrabberControl
#     startX = 2.47
#     endX = 1.81

#     @state(first=True)
#     def raiseArm(self, initial_call):
#         if initial_call:
#             self.logger.info(f'Raising arm to upper')
#             self.armControl.next_state('moveToUpper')
#         self.armControl.engage()
#         if self.armControl.last_state == 'atUpper':
#             self.next_state('moveBack')

#     @timed_state(duration=2, next_state='dropCone')
#     def moveBack(self, initial_call):
#         self.swerveChassis.fieldOrientedDrive(-0.125, 0, 0)
#         # self.swerveChassis.autoDrive()
#         # if self.swerveChassis.holonomicController.atReference():
#         #     self.next_state("dropCone")

#     @state()
#     def dropCone(self, initial_call):
#         if initial_call:
#             self.grabberControl.next_state('dropping')
#         self.grabberControl.engage()

#         if not self.grabberControl.hasObject:
#             self.next_state('moveForward')


#     @timed_state(duration=1, next_state='dropArm')
#     def moveForward(self, initial_call):
#         self.swerveChassis.fieldOrientedDrive(0.125, 0, 0)

#     @timed_state(duration=4, next_state='speedUp')
#     def dropArm(self, initial_call):
#         if initial_call:
#             self.armControl.next_state('moveToHome')
#             self.swerveChassis.fieldOrientedDrive(0,0,0)
#         self.armControl.engage()

#     @timed_state(duration=0.5, next_state='lockChassis')
#     def speedUp(self):
#         self.swerveChassis.fieldOrientedDrive(0.5, 0, 0)

#     @state()
#     def lockChassis(self, initial_call):
#         if initial_call:
#             self.swerveChassis.lockChassis()
#         self.armControl.engage()
#         if self.armControl.last_state == 'atHome':
#             self.next_state('end')

#     @state()
#     def end(self):
#         self.done()
