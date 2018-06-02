VoiceKBM
======================
This is a simple Python program that allows you to use voice commands to control your keyboard and mouse. I created it to develop my Python skills and learn about using APIs.

What it does
------------
There are many circumstances which may cause some people to have difficulty using regular mice and keyboards.
Other times, it would simply be more convenient if we could interact with our computer without having to use our hands, such as when cooking or eating. 

This program listens to the user for specific commands and carries out mouse or keyboard actions based on the given commands. The program currently supports mouse movement, mouse clicks and holding, mouse scrolling, typing, individual keyboard key pressing and holding, and keyboard shortcuts.

This is a fun little project I worked on, and it might not be perfect because I am only getting my feet wet. **I would highly appreciate any improvements and pull requests.**

How it works
------------
This program makes use of the Google Cloud Speech API wrapper from the Python SpeechRecognition library to continuously listen for and transribe designated voice commands (outlined in Instructions.txt) until the command to stop is given or the program is manually stopped.

The program parses the transcribed voice commands and uses the PyAutoGUI python module to programmatically control the mouse and keyboard. 

What you can do with this code
------------------------------
**You can feel free to fork this code, use it in your own programs, or whatever else you want to do with it.** If you decide to use this code in one of your own projects, please let me know as I'm interested to see what you do with it!

If you were to run this bot on your computer, here's what you would do:
- Download and install the latest version of [Python](https://www.python.org/downloads/). This program is working up to version 3.6.5
- Install [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/#) and [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- Run the program using this command from the directory you put it into:
    python VoiceKBM.py

**Ways to help me out:**
- The bot currently has trouble transcribing some voice commands partly because it exempts the first few fractions of a second of the voice command to measure and adjust for ambient/backgroud noise. Commands beginning with 'hold' in particular are commonly incorrectly transcribed. Maybe find a better way to handle the transcription.
- Make efficiency improvements in this program
- Add more commands.
- Report and fix any bugs you may encounter.