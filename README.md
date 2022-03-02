# FreenoveBigHexapod   
useful files for the Freenove Big Hexapod   

<h2> Hexapod Position Tool </h2>

HexaPosTool is a utility for converting the Freenove xyz co-ordinate system to servo angles or from servo angles to the co-ordinate system.  
It can store four positions and transition smoothly between them.  
Drop hexa_calibration.png, HexaPosTool.py and HexaPosToolui.py in the Code/Server directory.   
To run it type: <pre>python HexaPosTool.py</pre>
   
   
HexaPosToolui.ui is included in case someone wants to modify the UI   

<hr>

<h2> Local wireless keyboard and autonomous movement </h2>

The code has a dependancy for evdev (https://python-evdev.readthedocs.io/en/latest/): 

<ul>sudo pip3 install evdev</ul>

CAVEAT: I tidiesd up these files and removed modifications specific to my hexapod before uploading.
I was not able to test them. If you fix any errors or bugs please let me know and I will update the file(s) in question

This code was written for the "Rii i8S Mini Keyboard" available from Amazon

evdev sees this keyboard as 4 separate devices: a keyboard, a mouse, a consumer control and a system control

If you wish to use this code with other controllers or keyboards you may well have to comment out some of the devices and remap some of the keyboard associations

Drop the following 4 files into the Server directory on the Pi. You may want to backup your copy of Control.py first!

<pre>
wirelesskb.py      the keyboard reading routine - this is the one you run: sudo python wirelesskb.py
Control.py         modified version of the freenove file to enable scanning by the head when moving 
                   and collecting ultrasonic readings
Action.py          a couple of actions for the hexapod
wander.py          some dodgy autonomous movement code - needs a bit of tinkering, but my hexapod 
                   is currently undergoing modification so I can't test this
                   try adjusting these values
                      edgeDanger = 40
                      aheadClear = 50
                      obstDanger = 35
                      criticalEdge = 15
</pre>
<h3>Keyboard commands</h3>
<pre>
Trackpad      Move head
A             Head down
Q             Head up
Caps lock     Head left
S             Head right  
<br />
Up arrow      Move forward
Down arrow    Move backward
Left arrow    Turn left
Right arrow   Turn right 
Previous song Sideways left
Next song     Sideways right
<br />
Tab           Start/Stop autonomous movement
<br />
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

                    
