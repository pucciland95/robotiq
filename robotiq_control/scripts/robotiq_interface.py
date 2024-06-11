#!/usr/bin/env python
import rospy
from robotiq_msgs.msg import CModelCommand
from std_srvs.srv import Trigger
from time import sleep

class GripperController():
  
  def __init__(self):
    rospy.init_node('robotiq_controller')
    pub_command = rospy.Publisher('command', CModelCommand, queue_size=3)
    
    # TODO: obtain these from param file
    self.gripper_velocity = 255
    self.gripper_force = 150
    
    # TODO: get this from status value
    self.active = True
    
    # Instantiating services
    open_gripper_service = rospy.Service('open_gripper', Trigger, self.open_gripper)
    close_gripper_service = rospy.Service('close_gripper', Trigger, self.close_gripper)
    
  def open_gripper(self):
    self.check_is_active()
    command_open = self.gen_command_open()
    self.pub_command.pub(command_open)  
  
  def close_gripper(self):
    self.check_is_active()
    command_close = self.gen_command_close()
    self.pub_command.pub(command_close)
  
  ##########################################################
  ##################### Utils functions ####################
  ##########################################################
  
  def check_is_active(self):
    if self.active == False:
      command_activate = self.gen_command_activate()
      self.pub_command(command_activate)
    
  def gen_command_activate(self):
    command = CModelCommand()
    command.rACT = 1
    command.rGTO = 1
    command.rSP  = self.gripper_velocity
    command.rFR  = self.gripper_force
    return command

  def gen_command_open(self):
    command = CModelCommand()
    command.rPR = 0
    return command

  def gen_command_close(self):
    command = CModelCommand()
    command.rPR = 255
    return command
  
  
if __name__ == '__main__':
  
  gripper_controller = GripperController()
  rospy.spin()
  