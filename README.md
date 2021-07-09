# Master-Volume-control-using-Hand-Tracking-Module

This is Volume Control Project using Hand gestures .<br />
The Hand Connections were made using mediapipe library which was already implemented and used as handTrackModule.py <br />
The master Volume of the computer was connected using pycaw  
## Install

Latest stable release:
```bash
pip install pycaw
```
## Usage

```Python
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)
```

![](https://github.com/rohankumarp/Master-Volume-control-using-hand-Detection-Module/blob/main/Screenshot%202021-06-24%20143148.png)
![](https://github.com/rohankumarp/Master-Volume-control-using-hand-Detection-Module/blob/main/Screenshot%202021-06-24%20143300.png)
![](https://github.com/rohankumarp/Master-Volume-control-using-hand-Detection-Module/blob/main/camgif.gif)


Pycaw created by Andre Miras <br />
github Profile :- https://github.com/AndreMiras/pycaw
