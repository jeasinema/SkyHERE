#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# File Name : decos_interface.py
# Purpose :
# Creation Date : 15-03-2016
# Last Modified : Wed Mar 16 08:30:46 2016
# Created By : Jeasine Ma
# ---------------------------------
from functools import wraps
class decos():
    """
    This decos has 2 arguments,
    the first one is the minium of the args in the args tuple,
    the second one is the minium of the args in the kwargs dic.
    """
  
    def __init__(self, *args, **kwargs):
        #do somgthing
        self.decoargs = (list)(args)
        self.decokwargs = kwargs
        if len(self.decoargs) < 2:
            self.decoargs.append(0)

    def __call__(self, func):
        @wraps(func)
        def wrappers(*args, **kwargs):
            if len(args) < self.decoargs[0]:
                kwargs['tupvalid'] = False
            else:
                kwargs['tupvalid'] = True
            if len(kwargs) < self.decoargs[1]:
                kwargs['dicvalid'] = False
            else:
                kwargs['dicvalid'] = True
            return func(*args, **kwargs)
        return wrappers

