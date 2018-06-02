"""
Control the Mouse and Keyboard using voice commands
"""

import speech_recognition as sr
import pyautogui as pag
from typing import Dict, List


# TODO ADD SUPPORT FOR KEYBOARD FUNCTIONS


def read_mic_input(r: sr.Recognizer, mic: sr.Microphone) -> Dict:
    """Use r to transcribe speech recorded from mic, and return a dictionary
    containing three keys:

    "success": boolean value indicating whether or not the recognizer's speech
               transcription was successful or not
    "error": 'None' if no error occured, or a string containing the error
              message if an error occured.
    "transcription": 'None' if speech could not be transcribed, or a string
                      containing the transcribed text.
    """

    with mic as source:
        # adjust the recognizer sensitivity to account for ambient noise
        r.adjust_for_ambient_noise(source, duration=0.3)
        # Record voice input from microhpone
        audio = r.listen(source)

    # intialize the response dictionary to be returned
    response = {"success": True, "error": None, "transcription": None}

    # Attempt to recognize speech in the recording
    try:
        response["transcription"] = r.recognize_google(audio).lower()

        # clean up the transcription of coordinates and measurements
        response["transcription"] = response["transcription"].replace("-", " ")
        response["transcription"] = response["transcription"].replace("/", " ")
        response["transcription"] = response["transcription"].replace("\\", " ")
        response["transcription"] = response["transcription"].replace(" 00",
                                                                      " 0 0")

    # Update response object if a RequestError or UnknownValueError exception is
    #   caught
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "Error occurred with the API request."
    except sr.UnknownValueError:
        # speech could not be transcribed
        response["error"] = "Unable to recognize speech."

    return response


def move_mouse_relative(direction: str, distance: int) -> None:
    """
    Move the mouse in direction by distance pixels from the mouse's current
    position

    Precondition: direction is one of "up", "down", "left", "right"
    """
    if direction == "up":
        pag.moveRel(0, -distance, duration=1)
    elif direction == "down":
        pag.moveRel(0, distance, duration=1)
    elif direction == "left":
        pag.moveRel(-distance, 0, duration=1)
    elif direction == "right":
        pag.moveRel(distance, 0, duration=1)


def scroll(direction: str, amount: int) -> None:
    """
    Scroll in direction by amount

    Precondition: direction is one of 'up' or 'down'
    """
    if direction == "up":
        pag.scroll(amount)
    elif direction == "down":
        pag.scroll(-amount)


def perform_hotkey(keys: List[str]) -> None:
    """
    Hold down all the keyboard keys in keys and then release them all in reverse
    order.

    precondition: all elements of keys are in KEYBBOARD_KEYS
    """
    for k in keys:
        pag.keyDown(k)
    keys.reverse()
    for k in keys:
        pag.keyUp(k)


def correct_key_names(keys: List[str]) -> List[str]:
    """
    Return a List of strings containing the key name sin keys converted to forms
    which can be used by pyautogui functions.
    """
    joined = " ".join(keys)
    joined.replace("control", "ctrl")
    joined.replace("page down", "pagedown")
    joined.replace("page up", "pageup")
    joined.replace("volume down", "volumedown")
    joined.replace("volume up", "volumeup")
    joined.replace("page down", "pagedown")
    joined.replace("print screen", "printscreen")
    return joined.split()


def execute_command(parsed: List[str]) -> None:
    """
    Execute the command described in parsed.
    """
    parsed = correct_key_names(parsed)
    # get the mouse's current position
    x, y = pag.position()
    # check for "move to" command
    if parsed[0] == "move" and parsed[1] == "to":
        COMMANDS["move to"][0](int(parsed[2]), int(parsed[3]), duration=1)
    elif parsed[0] == "move":
        # must be a move up/down/left/right
        move_mouse_relative(parsed[1], int(parsed[2]))
    elif parsed[0] == "double" and parsed[1] == "click":
        # check for double click command
        COMMANDS["double click"][0](x, y)
    elif parsed[1] == "click":
        # must be a left, middle, or right click
        COMMANDS["left click"][0](x, y, button=parsed[0])
    elif parsed[0] == "hold" and parsed[1] in ["left", "middle", "right"]:
        # check for hold down mouse button
        COMMANDS["hold right"][0](x, y, button=parsed[1])
    elif parsed[0] == "release" and parsed[1] in ["left", "middle", "right"]:
        # check for release mouse button
        COMMANDS["release right"][0](x, y, button=parsed[1])
    elif parsed[0] == "scroll":
        COMMANDS["scroll up"][0](parsed[1], int(parsed[2]))
    elif parsed[0] == "type" and parsed[1] == "this":
        COMMANDS["type this"][0](" ".join(parsed[2:]), interval=0.05)
    elif parsed[1] == "key":
        COMMANDS[parsed[0] + " " + parsed[1]][0](parsed[2])
    elif parsed[0] == "use" and parsed[1] == "shortcut":
        perform_hotkey(parsed[2:])
    elif parsed[0] == "quit" and parsed[1] == "program":
        print("You said: quit program. Now quitting...")
        COMMANDS["quit program"][0]()


if __name__ == '__main__':
    # Set a dictionary of vocal commands to their respective functions
    pag.FAILSAFE = False
    COMMANDS = {"move to": (pag.moveTo, 4), "move up": (pag.moveRel, 3),
                "move down": (pag.moveRel, 3), "move left": (pag.moveRel, 3),
                "move right": (pag.moveRel, 3), "left click": (pag.click, 2),
                "double click": (pag.doubleClick, 2), "right click": (pag.click, 2),
                "middle click": (pag.click, 2), "hold left": (pag.mouseDown, 2),
                "hold right": (pag.mouseDown, 2), "hold middle": (pag.mouseDown, 2),
                "release left": (pag.mouseUp, 2), "release right": (pag.mouseUp, 2),
                "release middle": (pag.mouseUp, 2), "scroll up": (pag.scroll, 3),
                "scroll down": (pag.scroll, 3), "hold key": (pag.keyDown, 3),
                "release key": (pag.keyUp, 3), "press key": (pag.press, 3),
                "use shortcut": (pag.hotkey, 0), "type this": (pag.typewrite, 0),
                "quit program": (quit, 2)}

    KEYBOARD_KEYS = {'\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
                     ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
                     '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
                     'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
                     'browserback', 'browserfavorites', 'browserforward', 'browserhome',
                     'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
                     'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
                     'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                     'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                     'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                     'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
                     'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                     'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                     'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                     'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                     'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                     'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                     'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                     'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                     'command', 'option', 'optionleft', 'optionright'}

    # Instantiate recognizer and microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    exiting = False
    while not exiting:
        # Prompt user for a command
        print("Please say a voice command!")
        # Get a voice command from user and attempt to transcribe it
        command = read_mic_input(recognizer, microphone)
        if not command["success"]:
            # Unsuccessful transcription indicates an API request error
            print(command["error"])

        elif command["error"]:
            # API request was successful but speech could not be transcribed
            print("{} Please try saying that again.".format(command["error"]))

        if command["transcription"]:
            # find the base command without parameters
            parsed = command["transcription"].split()

            # show the user the command and execute it

            # manually check for "type this" command since it can have arbitrary
            # number of arguments
            if len(parsed) < 2:
                # Transcription was successful but command is invalid.
                print("{} is an invalid command. Please try another one!"
                      .format(command["transcription"]))
            else:
                base_command = parsed[0] + " " + parsed[1]

                if base_command == "type this" and len(parsed) > 2:
                    execute_command(parsed)
                    print("You said: {}. Executing command...".format(
                        command["transcription"]))
                elif base_command == "use shortcut" and len(parsed) > 2 and all(
                        [key in KEYBOARD_KEYS for key in parsed[2:]]):
                    execute_command(parsed)
                    print("You said: {}. Executing command...".format(
                        command["transcription"]))
                elif base_command in COMMANDS and "key" in base_command and len(
                        parsed) == COMMANDS[base_command][1] and parsed[2] in KEYBOARD_KEYS:
                    execute_command(parsed)
                    print("You said: {}. Executing command...".format(
                        command["transcription"]))
                elif base_command in COMMANDS and len(parsed) == COMMANDS[base_command][1] \
                        and all([x.isnumeric() for x in parsed[2:]]):
                    # other commands hae constant number of arguments
                    execute_command(parsed)
                    print("You said: {}. Executing command...".format(
                        command["transcription"]))

                else:
                    # Transcription was successful but command is invalid.
                    print("{} is an invalid command. Please try another one!"
                          .format(command["transcription"]))
