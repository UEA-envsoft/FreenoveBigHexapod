<h1>This folder contains code for expressions and claw movement.</h1>

This code is copied directly from my Hexapod and may have some values that are specific to my particular bot and will require adjustment.

Things to note:
My code is based around a very early implementation of the Freenove Hexapod and some things have changed.

I have updated my code to use the ADC.py file found in later implementations.

BorisKb.py is the file to run, it monitors the wireless keyboard and calls everything else.

Other new or modified files are also in this directory.

My code is for the freenove 8x16 led matrix.

If you are using the OPEN-SMART 0.8" Inch 16x8 I2C LED Dot Matrix you need to edit espressions.py:
<ul>
line 3 replace <tt>import freenove16x8matrix</tt> with <tt>import smart16x8matrix</tt>   <br />
line 8 replace <tt>self.display = freenove16x8matrix.freenove16x8matrix(address=0x71)</tt> with <tt>self.display = smart16x8matrix.smart16x8matrix(address=0x70)</tt>
</ul>
