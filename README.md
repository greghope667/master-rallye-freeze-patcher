# Master Rallye - Menu freeze patch

## About

The PC version of Master Rallye has an annoying bug where the menu transitions freeze for long periods of time, sometimes requiring an alt-tab command to resume the game. This is not a Windows 7/8/10 bug, it's existed on every system I've played the game on.
By applying a tiny (1-byte) patch to the executable I was able to bypass this bug. 
I've made a script to fix this in case anyone else still plays this game.

## How to install

1. Install Master Rally. This script applies to the executable from the 'fix' version of the game found on [My Abandonware](https://www.myabandonware.com/game/master-rallye-dpg).

1. Install Python (any 3.x version should work). On windows, I recommend the [Microsoft store](https://apps.microsoft.com/store/search?hl=en-us&gl=US&publisher=Python%20Software%20Foundation) for this.

2. Download this repository. On GitHub, click Code->Download ZIP. Extract the ZIP.

3. Right-click `freeze-patch.py` and open with Python.

4. Select the path to your `MRallye.exe` executable, press OK. Note that if you installed this game to a Program Files directory you may have to copy the executable elsewhere (e.g. Documents or Desktop) to be able to patch it. (You'll get a permissions error otherwise).

5. If you copied the executable, move it back to the original install location (overwrite the old, unpatched file).

6. Play Master Rallye - menu transitions should be much faster now, almost instant!

## How this works

The game has an internal flag telling it whether to advance the game/render the screen. During scene transitions this is set to false to avoid any wierd partial renders. The game should set this flag back to true when it is done loading, but doesn't do that very quickly (often taking many seconds, increasing every menu transition). I don't exactly know why, some bug in the loading logic maybe? Alt-tab forces the game to re-render so works around this bug. I edited the executable to skip this check and always re-render. Loads are now almost instant on my machine.

## Possible side effects

We've disabled the rendering pause during the load screens so the game may flicker in menu transitions. Potentially increases CPU/GPU load but none that I can measure for my system. Otherwise I've noticed no other side-effects from this.
