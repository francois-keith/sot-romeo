# -*- coding: utf-8 -*-
# Copyright 2011, Florent Lamiraux, Thomas Moulard, JRL, CNRS/AIST
#
# This file is part of dynamic-graph.
# dynamic-graph is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# dynamic-graph is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# dynamic-graph. If not, see <http://www.gnu.org/licenses/>.

from dynamic_graph.sot.dynamics.humanoid_robot import AbstractHumanoidRobot
from dynamic_graph.ros import RosRobotModel

# Sot model for the romeo_small.urdf (with gripper, no fingers)
class Robot (AbstractHumanoidRobot):
    """
    This class instanciates Aldebaran Romeo robot
    """
    halfSitting = (
        0, 0, 0.840252, 0, 0, 0,                         # Free flyer
        0, 0, -0.3490658, 0.6981317, -0.3490658, 0, 0,   #  Left leg
        0, 0, -0.3490658, 0.6981317, -0.3490658, 0, 0,   #  Right leg
        0,                                               #  Trunk
        1.5, 0.6, -0.5, -1.05, -0.4, -0.3, -0.2,         #   Left arm
        0, 0, 0, 0,                                      #   Head
        0, 0 ,0 ,0,                                      #    Eyes
        1.5, -0.6, 0.5, 1.05, -0.4, -0.3, -0.2,          #   Right arm
    )

    jointMap = { }
    jointMap['BODY'] = 'body'

    def __init__(self, name, 
                 device = None,
                 tracer = None):
        AbstractHumanoidRobot.__init__ (self, name, tracer)
        self.urdfDir  = 'package://romeo_description/urdf/'
        self.urdfName = 'romeo_small.urdf'


        self.OperationalPoints.append('waist')
        self.OperationalPoints.append('chest')
        self.device = device

        # correct the name of the body link
        self.dynamic = RosRobotModel("{0}_dynamic".format(name))
        for i in self.jointMap:
            self.dynamic.addJointMapping(i, self.jointMap[i])
        self.dynamic.loadUrdf(self.urdfDir + self.urdfName)

        # complete feet position (TODO: move it into srdf file)
        ankle =self.dynamic.getAnklePositionInFootFrame()
        self.ankleLength = 0.1935
        self.ankleWidth  = 0.121

        self.dynamic.setFootParameters(True , self.ankleLength, self.ankleWidth, ankle)
        self.dynamic.setFootParameters(False, self.ankleLength, self.ankleWidth, ankle)

        # check half sitting size
        self.dimension = self.dynamic.getDimension()
        if self.dimension != len(self.halfSitting):
            raise RuntimeError("invalid half-sitting pose")
        self.initializeRobot()

__all__ = ["Robot"]
