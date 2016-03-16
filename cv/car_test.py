#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# File Name : 2.py
# Purpose :
# Creation Date : 16-03-2016
# Last Modified : Wed Mar 16 15:21:25 2016
# Created By : Jeasine Ma
# ---------------------------------

from  move_interface import carHandle as myc

while(True):
    car = myc(0,9600)
    car.send_cmd(0,20)
    car.wait_button(0,'s')
