#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# File Name : decos_interface.py
# Purpose :
# Creation Date : 15-03-2016
# Last Modified : Wed Mar 16 16:54:06 2016
# Created By : Jeasine Ma
# ---------------------------------
from functools import wraps
class decos():
    """
    This deco has 2 arguments,
    the first one is the minium of the args in the args tuple,
    the second one is the minium of the args in the kwargs dic.
    !!ATTENTION!!
    if the function you want to decorate is a member of a class, please remeber it will have an argument "self" neverthelessly
    so line 33 and 37 must "+1" , we set it as default
    TODO:
    fix this bug in a smarter way.
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
#            print "len(args)", len(args)
#            print "decoargs",self.decoargs
            if len(args) < self.decoargs[0] + 1:
                kwargs['tupvalid'] = False
            else:
                kwargs['tupvalid'] = True
            if len(kwargs) < self.decoargs[1] + 1:
                kwargs['dicvalid'] = False
            else:
                kwargs['dicvalid'] = True
            return func(*args, **kwargs)
        return wrappers

if __name__ == "__main__":
    pass

