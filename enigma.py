""" 
M3 Enigma Wheels -- http://www.cryptomuseum.com/crypto/enigma/m3/index.htm:
Wheel	ABCDEFGHIJKLMNOPQRSTUVWXYZ	Notch(es)	Turnover
ETW	    ABCDEFGHIJKLMNOPQRSTUVWXYZ	 	 	 
I	    EKMFLGDQVZNTOWYHXUSPAIBRCJ	Y	        Q
II	    AJDKSIRUXBLHWTMCQGZNPYFVOE	M	        E
III	    BDFHJLCPRTXVZNYEIWGAKMUSQO	D	        V
IV	    ESOVPZJAYQUIRHXLNFTGKDCMWB	R	        J
V   	VZBRGITYUPSDNHLXAWMJQOFECK	H	        Z
-- naval only here down ---
VI	    JPGVOUMFYQBENHZRDKASXLICTW	HU	        ZM
VII	    NZJHGRCXMYSWBOUFAIVLPEKQDT	HU  	    ZM
VIII	FKQHTLXOCBJSPDZRAMEWNIUYGV	HU	        ZM
UKW-B	YRUHQSLDPXNGOKMIEBFZCWVJAT	 	 	 
UKW-C	FVPJIAOYEDRZXWGCTKUQSBNMHL	 	 	 
"""
rotors = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ','AJDKSIRUXBLHWTMCQGZNPYFVOE','BDFHJLCPRTXVZNYEIWGAKMUSQO','ESOVPZJAYQUIRHXLNFTGKDCMWB','VZBRGITYUPSDNHLXAWMJQOFECK']
reflectors = {"B":'YRUHQSLDPXNGOKMIEBFZCWVJAT', "C":'FVPJIAOYEDRZXWGCTKUQSBNMHL'}
rotorPositions = [1, 1, 1]  # define initial positions of rotors
rotorStack = [4, 3, 1]      # define initial rotors to use in the stack

def incrementRotor():
    """Routine to increment the rotorPositions[] array
    """
    rotorCount = len(rotorPositions)-1
    rotorPositions[rotorCount] += 1
    # TODO: Make rotors increment if necessary.

def rotorReturn(input='A',rotor=1, rotorPos=3):
    """Run a character through a single rotor

    Keyword arguments:
    input -- character to pass through the rotor
    rotor -- the rotor number to run the input through
    rotorPos -- the position of the rotor in the Enigma
    """
    if (rotorPos > len(rotorStack)):
        rotorPos = len(rotorStack)
        print("Resetting rotor position to "+str(rotorPos))
    if (rotor > len(rotors)): return  # return nothing if we're higher than a valid rotor
    offset = ord('A')
    #print("Sending " + input.upper() + " to rotor " + str(rotor) + " in position " + str(rotorPos))
    return(rotors[rotor-1][ord(input.upper())-offset])

def reflectorReturn(input,reflector='B'):
    """Run a character through the reflector.

    Keyword arguments:
    input -- character to pass through the reflector
    reflector - Which UKW version of reflector (valid: B or C, default B)
    """
    if (reflector.upper() not in ["B","C"]):
        reflector = "B"
        print("Resetting reflector to valid choice")
    offset = ord('A')
    output = reflectors[reflector][ord(input.upper())-offset]
    #print("Reflector "+reflector+" received "+input+", reflector returned "+output)
    return(output)

def encipherStack(rotorStack=[1,2,3], input='A'):
    """Run a character through the rotor stack

    Keyword arguments:
    rotorStack -- list[] of rotors (left-to-right) to run the input through. Actual Engimas supported 3 or 4 rotors, this supports an infinite length list.
    input -- character to pass through the stack
    """
    rotorStack.reverse()
    """ reverse() it so you go right-to-left; Enigma signals start on right side of machine """
    counter = len(rotorStack)   # track which rotor we're operating on at the moment
    for f in rotorStack:
        input = rotorReturn(input, f, counter)
        counter -= 1
    input = reflectorReturn(input)
    rotorStack.reverse()
    counter = 1
    for f in rotorStack:
        """ reverse() it again to bring it back left-to-right """
        input = rotorReturn(input, f, counter)
        counter += 1
    incrementRotor()
    print(rotorPositions)
    return(input)


for c in range(65, 91):
    print("Sending "+chr(c)+" to Enigma. Output is "+encipherStack(rotorStack, chr(c)))
        

