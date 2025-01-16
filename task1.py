import binascii
import codecs

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
        return inp, freq
    return None, None

def findString(file):
    possibleStrings = []
    freqList = []
    f = open(file, 'r')
    for line in f:
        check, freq = isEnglish(line, 1.73)
        if check:
            possibleStrings.append(line)
            freqList.append(freq)
    return possibleStrings, freqList

def charXOR(inp, key):
    result = ''
    sepInp = [inp[i:i + 8] for i in range(0, len(inp), 8)]
    for byte in sepInp:
        bth = byteToHex(xor(byte,key))
        result += hexToAscii(bth)
    return result

def stringToHex(inp):
    return inp.encode('utf-8').hex()


result, freqResult = findString('Lab0.TaskII.B.txt')

for i in range(len(freqResult)):
    mostCommonChar = max(freqResult[i], key=freqResult[i].get)
    potKeys = [] 
    potKeys.append(xor(hexToByte(mostCommonChar), hexToByte(stringToHex(" "))))
    potKeys.append(xor(hexToByte(mostCommonChar), hexToByte(stringToHex("e"))))
    potKeys.append(xor(hexToByte(mostCommonChar), hexToByte(stringToHex("E"))))
    bitsFH = hexToByte(result[i])
    for keys in potKeys:
        print("Using key: "+keys+"\n"+charXOR(bitsFH, keys)+"\n\n")


