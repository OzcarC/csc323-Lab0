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
            except ValueError:
                continue

def multiByteXor(fileName):
    return None

def everyXHex(inp, start, step):
    ans = ""
    for i in range(start*2, len(inp), step*2):
        ans+=inp[i:i+2]
    return ans

def findKeyLen(inp):
    workingStrs = []
    sepInp = [inp[i:i + 2] for i in range(0, len(inp), 2)]
    for i in range(1,10,1):
        if len(workingStrs) < i:
            workingStrs.append("")
        for j in range(0, len(sepInp), i):
            workingStrs[i-1] += sepInp[j]
    m = -10
    mFreq = {}
    mLen = 0
    mInp = ""
    for i in range(len(workingStrs)):
        scored, freq = isEnglish(workingStrs[i], 1.73)
        if scored and scored > m:
            m, mFreq, mLen, mInp = scored, freq, i+1, workingStrs[i]
    return mLen, mInp, mFreq

# singleByteXor('Lab0.TaskII.B.txt')

test = byteToHex(b64ToBin("LhfQy3oVDtrLehURx4I/QRjbg3oVFpWTMgRZ04h9ayrbiDURWfGIPQYAlaM1Bh6VhjQFWfGVdEE9x4J6CAqVhi5BDd2CegUW2pVQMxzUgyNBDdrHNwAS0Mc7D1nQiS4TGNuEP0EK2sc4ABrexzUPWcCXUEk61JIpBFnMiC9BEtuILUEO0MAoBFnUhTUUDZWTNUEL3Jd6Eg3AgTxBDMXOems+3JE/QRTQxy4JHJWKMwIL2pcyDhfQxzwIC8aTehIWla56AhjbxzgUCsHHNggS0Mc7QRvAhTgNHL+kNQwJwYg0QRjbg3otFtuAeiMc1IQyQQ3agD8VEdCVeg8WwscjDgyVjDQODpWeNRRZ3Il6FQvakjgNHL+mMw9ewcc0Dg3djjQGWdeSLkEYlaB6FRHUiT1NWdeGOBhZv7MtDlnZiDlGHNHHNRQNlYMvBRzGxykOWcKCfRMclYQoAAPM7R4EGMGPejMWwsczElnBjz9BFdSFPw1ZwY87FVnFhiMSWdiCUDQX04Y+BBjXiz9BCtrHKg0c1JQ/QR3aiX0VWcGVI0EN2sc8AB3Qxy4JEMbt"))
length, keyedStr, keyedFreq = findKeyLen(test)
decStrings = []

for i in range(0, length, 1):
    keyedStr = "".join(everyXHex(test, i, length))
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
                print("Using key: " + keys + "\t on shift #" +str(i)+ "\n" + msg + "\n\n________________________")
            except ValueError:
                print("Failed Using key "+keys+" on iteration #"+str(i)+"\n\n________________________")
            except Exception:
                print("Likely not english. Using key "+keys+" on iteration #"+str(i)+"\n\n________________________")
            else:
                decStrings.append(msg)

longest = max(decStrings, key=len)
for decStr in decStrings:

print(decStrings)