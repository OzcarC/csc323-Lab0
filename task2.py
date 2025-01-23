import binascii
import codecs
import base64

def byteToHex(byte):
    bits = hex(int(byte,2))[2:]
    return bits

def hexToByte(hex):
    ans = ""
    for i in range(0,(len(hex)),2):
        try:
            temp = bin(int(hex[i:i+2],16))[2:].zfill(8)
        except ValueError:
            temp = ""
        else:
            ans += temp
    return ans

def hexToInt(hex):
    return int(hex,16)
def b64ToBin(inp):
    dec = base64.b64decode(inp)
    dec = "".join(["{:08b}".format(x) for x in dec])
    return dec

def hexToAscii(hex):
    if len(hex) == 1:
        hex = hex.rjust(2,"0")
    return bytes.fromhex(hex).decode('utf-8')

def xor(inp, key):
    outp = ''
    if len(inp) > len(key):
        while len(inp) > len(key):
            key += key
    for i in range(len(inp)):
        if inp[i] == key[i]:
            outp += '0'
        else:
            outp += '1'
    return outp

def score(inp):
    freq = {}
    normCoeff = 26
    sum = 0
    sepInp = [inp[i:i+2] for i in range(0, len(inp), 2)]
    bigN = 0
    for byte in sepInp:
        freq[byte] = freq.get(byte, 0) + 1
    for byte in freq:
        sum += freq[byte]*(freq[byte]-1)
        bigN += freq[byte]
    ic = (normCoeff*sum)/(bigN*(bigN-1))
    return ic, freq

def isEnglish(inp, exp):
    scored,freq = score(inp)
    if (exp-0.5) <= scored <= (exp+0.5):
        return scored, freq
    return None, None

def findString(file):
    possibleStrings = []
    freqList = []
    f = open(file, 'r')
    for line in f:
        score, freq = isEnglish(line, 1.73)
        if score:
            possibleStrings.append(line)
            freqList.append(freq)
    return possibleStrings, freqList

def charXOR(inp, key):
    result = ''
    sepInp = [inp[i:i + 8] for i in range(0, len(inp), 8)]
    for byte in sepInp:
        bth = byteToHex(xor(byte,key))
        charVal = int(bth, 16)
        if (32<= charVal <= 126) or (charVal == 10):
            result += hexToAscii(bth)
        else:
            raise Exception("Character out of range")
    return result

def stringToHex(inp):
    return inp.encode('utf-8').hex()

def singleByteXor(fileName):
    result, freqResult = findString(fileName)
    for i in range(len(freqResult)):
        mostCommonChar = max(freqResult[i], key=freqResult[i].get)
        potKeys = []
        commonChars = [' ', 'e','E', 't', 'T', 'a','A']
        for commChar in commonChars:
            potKeys.append(xor(hexToByte(mostCommonChar), hexToByte(stringToHex(commChar))))
        bitsFH = hexToByte(result[i])
        for keys in potKeys:
            try:
                print("Using key: " + keys + "\n" + charXOR(bitsFH, keys) + "\n\n")
            except Exception:
                continue

def multiByteXor(fileName):
    f = open(fileName, 'r')

    ciphertext = byteToHex(b64ToBin(f.read()))
    info = findKeyLen(ciphertext, 10)
    decStrings = []
    for tup in info:
        length = tup[0]
        for i in range(0, length, 1):
            keyedStr = "".join(everyXHex(ciphertext, i, length))
            scored, keyedFreq = score(keyedStr)
            if scored:
                mostCommonChar = max(keyedFreq, key=keyedFreq.get)
                potKeys = []
                commonChars = [' ', 'e', 'E', 't', 'T', 'a', 'A']
                for commChar in commonChars:
                    potKeys.append(xor(hexToByte(mostCommonChar), hexToByte(stringToHex(commChar))))
                bitsFH = hexToByte(keyedStr)
                for keys in potKeys:
                    try:
                        msg = charXOR(bitsFH, keys)
                        # print("Using key: " + keys + "\t on shift #" + str(i) + "\n" + msg + "\n\n________________________")
                    except ValueError:
                        # print("Failed Using key " + keys + " on iteration #" + str(i) + "\n\n________________________")
                        continue
                    except Exception:
                        # print("Likely not english. Using key " + keys + " on iteration #" + str(i) + "\n\n________________________")
                        continue
                    else:
                        decStrings.append(msg)

        longest = len(max(decStrings, key=len))
        fullString = []
        for i in range(longest):
            for decStr in decStrings:
                if i < len(decStr):
                    fullString.append(decStr[i])
        fullString = "".join(fullString)

        print(fullString)

def everyXHex(inp, start, step):
    ans = ""
    for i in range(start*2, len(inp), step*2):
        ans+=inp[i:i+2]
    return ans

def findKeyLen(inp, amount):
    possibleInfo = []
    workingStrs = []
    sepInp = [inp[i:i + 2] for i in range(0, len(inp), 2)]
    for i in range(1,amount,1):
        if len(workingStrs) < i:
            workingStrs.append("")
        for j in range(0, len(sepInp), i):
            workingStrs[i-1] += sepInp[j]
    # m = 10
    # mFreq = {}
    # mLen = 0
    # mInp = ""
    for i in range(len(workingStrs)):
        scored, freq = isEnglish(workingStrs[i], 1.73)
        if scored: #and abs(scored-1.73) < m:
            info = (i+1, freq, workingStrs[i])
            possibleInfo.append(info)
    return possibleInfo

def shift(inp, amount):
    shifted = inp + amount
    if shifted < 65:
        shifted += 26
    elif shifted > 90:
        shifted -= 26
    return shifted

def vigCipher(filename):
    f = open(filename)

    ciphertext = stringToHex(f.read())
    info = findKeyLen(ciphertext,10)
    bestLength = info[0][0]
    lengths = []
    for currLen in range(bestLength,bestLength*5, bestLength):
        lengths.append(currLen)
    for length in lengths:
        decStrings = []
        key = ""
        for i in range(0, length, 1):
            keyedStr = everyXHex(ciphertext,i,length)
            scored, keyedFreq = score(keyedStr)
            keyedStr = [hexToInt(keyedStr[j:j+2]) for j in range(0, len(keyedStr), 2)]
            if scored > -1:
                mostCommonChar = hexToInt(max(keyedFreq, key=keyedFreq.get))
                potKeys = []
                commonChars = [j for j in range(65,91,1)]
                for commChar in commonChars:
                    potKeys.append(commChar-mostCommonChar)
                minWeirdCount = len(keyedStr) + 1
                maxGoodCount = 0
                bestMsg = "Too Weird"
                shifted = 0
                bestKey = 'A'
                for keys in potKeys:
                    msg = "".join([chr(shift(s,keys)) for s in keyedStr])
                    weirdCount = msg.count("Z") + msg.count("Q") + msg.count("X") + msg.count("J")
                    goodCount = msg.count("E") + msg.count("T") + msg.count("A") + msg.count("O")
                    if goodCount/(weirdCount+1) > maxGoodCount/(minWeirdCount+1):
                        bestMsg = msg
                        minWeirdCount = weirdCount
                        maxGoodCount = goodCount
                        shifted = keys
                        if(shifted > 0):
                            shifted = 26-keys
                        bestKey = chr(abs(shifted)+65)
                key+=bestKey
                # print("Using shift: " + str(shifted) + "\t on char number:" + str(i) + "\n" + bestMsg + "\n\n________________________")
                decStrings.append(bestMsg)

        longest = len(max(decStrings, key=len))
        fullString = []
        for i in range(longest):
            for decStr in decStrings:
                if i < len(decStr):
                    fullString.append(decStr[i])
        fullString = "".join(fullString)
        print("\n________________________________________\nUsing Key: "+key+" message:\n"+fullString)

singleByteXor('Lab0.TaskII.B.txt')
multiByteXor('Lab0.TaskII.C.txt')
vigCipher('Lab0.TaskII.D.txt')