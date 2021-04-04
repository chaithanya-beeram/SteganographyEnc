
def caesarEncode(data, delay):
    result = ""
    opt = data.split(" -")
    data = opt[2]
    result += "-c -" + str(delay) + " -"
    for letter in data:
        if (letter.isalpha()):
            if letter.isupper():
                result += chr((ord(letter) + delay - 65) % 26 + 65)
            else:
                result += chr((ord(letter) + delay - 97) % 26 + 97)
        else:
            result += letter
    return result

def caesarDecode(data, delay):
    result = ""

    for letter in data:
        if (letter.isalpha()):
            if letter.isupper():
                result += chr((ord(letter) - delay - ord('A')) % 26 + ord('A'))
            else:
                result += chr((ord(letter) - delay - ord('a')) % 26 + ord('a'))
        else:
            result += letter
    return result

def vigenereEncode(data, delay):
    delayList = []
    delay = delay.upper()
    for letter in delay:
        if letter.isalpha():
            delayList.append(ord(letter) - ord('A'))
        else:
            delayList.append(0)

    length = len(delayList)
    result = ""
    count = 0
    opt = data.split(" -")
    data = opt[2]
    result += "-v -" + delay + " -"
    for letter in data:
        if (letter.isalpha()):
            if letter.isupper():
                result += chr((ord(letter) + delayList[count % length] - 65) % 26 + 65)
            else:
                result += chr((ord(letter) + delayList[count % length] - 97) % 26 + 97)
            count += 1
        else:
            result += letter
    return result

def vigenereDecode(data, delay):
    delayList = []
    delay = delay.upper()
    for letter in delay:
        if letter.isalpha():
            delayList.append(ord(letter) - ord('A'))
        else:
            delayList.append(0)

    length = len(delayList)
    result = ""
    count = 0
    for letter in data:
        if (letter.isalpha()):
            if letter.isupper():
                result += chr((ord(letter) - delayList[count % length] - 65) % 26 + 65)
            else:
                result += chr((ord(letter) - delayList[count % length] - 97) % 26 + 97)
            count += 1
        else:
            result += letter
    return result
