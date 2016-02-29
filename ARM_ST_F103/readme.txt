Using CodeSourcery to build project for STM32F10x cortex-M3 core microcontroller

By  Qibo Zhang (Michael) China
Email: sudazqb@163.com
MSN  : zhangqibo_1985@hotmail.com
DATE : 2007-12-20

// why CodeSourcery?
// WinARM do not support cortex-M3, keil iar does, but they are not free. So I found this, but sadly there is 
// demo code of this enviroment, so I decide to create one. 
// Thanks to WinARM's author: Martin Thomas.   His ARMv7 Project is my reference, the structure of this demo 
// is based on hisproject 

Readme file:

How to use the code?

Step 1: install toolchain

You should install a CodeSourcery GNU toolchain first.
Pls visit: http://www.codesourcery.com/
exactly the download page: http://www.codesourcery.com/gnu_toolchains/arm/download.html
to download the latest version software.

Lite edition codesourcery only support command line, and it is totaly free!

After install the software, then you need to rboot your computer.


Step 2: build the library

Under commandline, enter ../library/src of this demo
just type make, and everything will be done.

Step 3: build the image

enter ../project/codesourcery and then make
done!

it will create main.bin file, use ST's flash loader to download the image


Good Luck!

Qibo Zhang (michael) China   2007-12-20
 