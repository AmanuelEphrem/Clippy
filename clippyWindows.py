import pyperclip
import time
from pynput.keyboard import Key, Listener

#essential variables to use during program
storedKeys = []
cmdCharacters = ["'c'"]
ctrlCharacters = ["'1'", "'2'","'3'","'4'","Key.ctrl"]
numKeys = 0

#greeting to user
print("Hello, my name is Clippy!")
print("Ctrl + C to copy")
print("Alt + 1,2,3,4 to choose what to copy")
print("Ctrl + V to paste")
print("Ctrl + Alt to clear all your copies")
print("Esc to exit")

#defines acceptable key sequences
def actOnKey(stored):
    global numKeys
    # defines (ctrl + c)
    if stored[0] == Key.ctrl and str(stored[1]) == "'c'":
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
    elif stored[0] == Key.alt and stored[1] != Key.ctrl:
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
    elif stored[0] == Key.ctrl and stored[1] == Key.alt:
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
    if len(storedKeys) == 0 and key != Key.ctrl and key != Key.alt:
        pass
    elif len(storedKeys) == 1 and storedKeys[0] == Key.ctrl:
        if key == Key.ctrl:
            pass
        elif str(key) not in cmdCharacters:
            storedKeys.clear()
        else:
            storedKeys.append(key)
    elif len(storedKeys) == 1 and storedKeys[0] == Key.alt:
        if key == Key.alt:
            pass
        elif str(key) not in ctrlCharacters:
            storedKeys.clear()
        else:
            storedKeys.append(key)
    else:
        storedKeys.append(key)

    #stored keys are either (cmd, characters specified) or (ctrl, characters specified)
    if len(storedKeys) == 2:
        #print(storedKeys)
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
listener.join()
