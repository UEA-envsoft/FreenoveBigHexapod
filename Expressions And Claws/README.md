<h1>This folder contains code for expressions and claw movement.</h1>

This code is copied directly from my Hexapod and may have some values that are specific to my particular bot and will require adjustment.

Things to note:
My code is based around a very early implementation of the Freenove Hexapod and some things have changed.

I have updated my code to use the ADC.py file found in later implementations.

BorisKb.py is the file to run, it monitors the wireless keyboard and calls everything else.

![image](https://github.com/UEA-envsoft/FreenoveBigHexapod/assets/64538329/b358bf63-ae10-4306-9c24-0cde73722713) I use the Rii i8s mini keyboard

My Servo Connections:    
   
2 - Left Claw   
3 - Right Claw   
4 - Left Arm   
5 - Right Arm   
6 - Left Wrist   
7 - Right Wrist   


Other new or modified files are also in this directory.

My code is for the freenove 8x16 led matrix.

If you are using the OPEN-SMART 0.8" Inch 16x8 I2C LED Dot Matrix you need to edit espressions.py:
<ul>
line 3 replace <tt>import freenove16x8matrix</tt> with <tt>import smart16x8matrix</tt>   <br />
line 8 replace <tt>self.display = freenove16x8matrix.freenove16x8matrix(address=0x71)</tt> with <tt>self.display = smart16x8matrix.smart16x8matrix(address=0x70)</tt>
</ul>

Please let me know of any problems, such as other necessary files that I may have forgotten to upload!

<h3>Keyboard commands</h3>
<pre>
Trackpad      Move head
A             Head down
Q             Head up
Caps lock     Head left
S             Head right  
 
W             Left arm left
E             Left arm right
I             Right arm left
O             Right arm right
D             Left claw open
F             Left claw close
K             Right claw open
L             Right claw close
 
Up arrow      Move forward
Down arrow    Move backward
Left arrow    Turn left
Right arrow   Turn right 
Previous song Sideways left
Next song     Sideways right
 
Tab           Start/Stop autonomous movement
 
B             Beep
R             Relax
<br />
1 to 0        Speed
<br />
F1            Action rear up
F2            Action rear up and waggle front legs
<br />
Win key       Exit program
End key       Shutdown Pi
SysRq key     Reboot Pi
</pre>
