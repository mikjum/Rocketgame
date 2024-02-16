# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 15:22:30 2024

@author: Mikko
"""
import math

def introduce_force(angle, thrust, throttle):
    total_force = thrust + throttle
    acceleration = [-total_force*math.sin(math.radians(angle)), -total_force * math.cos(math.radians(angle)) ]
    return acceleration

def update_speed(speed, acceleration):
    speed[0] += acceleration[0]
    speed[1] += acceleration[1]
    return speed

def introduce_external_force(acceleration, force):
    acceleration[0] +=force[0]
    acceleration[1] += force[1]
    return acceleration

def introduce_friction(speed, friction):
    direction_angle = math.degrees(math.atan2(speed[1], speed[0]))
    friction_angle = direction_angle - 180
    return direction_angle, friction_angle