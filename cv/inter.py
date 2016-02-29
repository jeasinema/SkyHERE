# -*- coding: UTF-8 -*-
import os
data = []
no = 15
while(True):
    name = raw_input("name\n")
    if name == "ok":
        break
    count = raw_input("count\n")
    prize = raw_input("prize\n")
    reason = raw_input("reason\n")
    no =no + 1
    item = "|2.23|"+(str)(no)+"|马晓健|项目|SkyHERE|"+(str)(name)+"|"+(str)(count)+"|"+(str)(prize)+"|"+reason+"\n"
    print item
    data.append(item)
print data


