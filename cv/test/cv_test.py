#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# ----------------------------------
# @File Name : 1.py
# @Purpose :
# @Creation Date : 14-03-2016
# @Last Modified : Wed Mar 16 08:25:54 2016
# @Created By : Jeasine Ma
# ---------------------------------
from decos_interface import decos  
from functools import wraps
def check_args(*arg):
    print '1'
    def real_deco(func):
        print '2'
        @wraps(func)
        def wrappers(*args, **kwargs):
            #do something
            print '3'
            print args,kwargs
            if len(kwargs) < arg[1]:
                kwargs['dicvalid'] = False
            else:
                kwargs['dicvalid'] = True
            if len(args) < arg[0]:
                kwargs['tupvalid'] = False
            else: 
                kwargs['tupvalid'] = True
            return func(*args, **kwargs)
        return wrappers
    return real_deco

#def decos(*arg):
#    def decos_real(func):
#        print arg
#        func()   #the same as directly call the func()
#    return decos_real
#

        
       
#@check_args(2,1)
@decos(1)
def func1(*args, **kwargs):
    print kwargs

@decos(1)
def func2(*args, **kwargs):
    print kwargs
    return 1
func1(1,2,my=3)
a = func2()
print a
