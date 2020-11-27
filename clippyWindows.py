import pyperclip
import time
from pynput.keyboard import Key, Listener

#essential variables to use during program
storedKeys = []
cmdCharacters = ["'c'","Key.shift"]
ctrlCharacters = ["'1'", "'2'","'3'","'4'","Key.ctrl_l"]
numKeys = 0

#greeting to user
print("Hello, my name is Clippy!")
print("First copy using Ctrl+C, then type Ctrl+Shift to store it")
print("Alt + 1,2,3,4 to choose what to copy")
print("Ctrl + V to paste")
print("Alt + Ctrl to clear all your copies")
print("Esc to exit")

#defines acceptable key sequences
def actOnKey(stored):
    global numKeys
    # defines (ctrl + c)
    if stored[0] == Key.ctrl_l and str(stored[1]) in cmdCharacters:
        #waits to make sure copy is in clipboard
        time.sleep(0.1)
        #stores to text file and encodes spaces as a special character
        copy = str(pyperclip.paste()).replace("\n","!!~!!")
        if copy != "" and not copy.isspace():
            with open("clippyText.txt", "a") as f:
                if numKeys < 4:
                    f.write(copy)
                    f.write("\n")
                    numKeys += 1
                    f.close()
    # defines (alt + 1,2,3,4)
    elif stored[0] == Key.alt_l and stored[1] != Key.ctrl_l:
        with open("clippyText.txt", "r") as file:
            content = list(file)
            #removes quotes from keyboard
            for x in range(0, len(content)):
                content[x] = str(content[x]).replace("\n","")
            #copies to clipboard
            index = ctrlCharacters.index(str(stored[1]))
            if index < len(content):
                pyperclip.copy(str(content[index]).replace("!!~!!","\n"))
    # defines (ctrl + alt)
    elif stored[0] == Key.alt_l and stored[1] == Key.ctrl_l:
        #clears text file
        with open("clippyText.txt", "w") as file:
            file.truncate(0)
            numKeys = 0
            # waits to make sure copy is in clipboard
            time.sleep(0.1)
            file.close()

#checks if correct keys are pressed. If so it will do a action. If not then nothing will happen
def press(key):
    #makes sure only correct keys are being checked (cmd, characters specified) or (ctrl, characters specified)
    if len(storedKeys) == 0 and key != Key.ctrl_l and key != Key.alt_l:
        pass
    elif len(storedKeys) == 1 and storedKeys[0] == Key.ctrl_l:
        if key == Key.ctrl_l:
            pass
        elif str(key) not in cmdCharacters:
            storedKeys.clear()
        else:
            storedKeys.append(key)
    elif len(storedKeys) == 1 and storedKeys[0] == Key.alt_l:
        if key == Key.alt_l:
            pass
        elif str(key) not in ctrlCharacters:
            storedKeys.clear()
        else:
            storedKeys.append(key)
    else:
        storedKeys.append(key)

    #stored keys are either (cmd, characters specified) or (ctrl, characters specified)
    if len(storedKeys) == 2:
        actOnKey(storedKeys)
        storedKeys.clear()


# clears text file when program ends using the esc key
def release(key):
    if key == Key.esc:
        with open("clippyText.txt", "w") as file:
            file.truncate(0)
            file.close()
        return False

#listener thread for keyboard
listener = Listener(on_press=press, on_release=release)
listener.start()
#anticipates KeyboardInterrupt exception being raised
try:
  listener.join()
except KeyboardInterrupt as e:
  #this exception is expected because script is intended to be in the background
  #the user will constantly "interrupt" the program during execution and that is intended
  pass
