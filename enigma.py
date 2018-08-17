""" 
M3 Enigma Wheels -- http://www.cryptomuseum.com/crypto/enigma/m3/index.htm :
Wheel	ABCDEFGHIJKLMNOPQRSTUVWXYZ	Notch(es)	Turnover
I	    EKMFLGDQVZNTOWYHXUSPAIBRCJ	Y	        Q
II	    AJDKSIRUXBLHWTMCQGZNPYFVOE	M	        E
III	    BDFHJLCPRTXVZNYEIWGAKMUSQO	D	        V
IV	    ESOVPZJAYQUIRHXLNFTGKDCMWB	R	        J
V   	VZBRGITYUPSDNHLXAWMJQOFECK	H	        Z
-- naval only here down --
VI	    JPGVOUMFYQBENHZRDKASXLICTW	HU	        ZM
VII	    NZJHGRCXMYSWBOUFAIVLPEKQDT	HU  	    ZM
VIII	FKQHTLXOCBJSPDZRAMEWNIUYGV	HU	        ZM
-- reflectors --
UKW-A   EJMZALYXVBWFCRQUONTSPIKHGD
UKW-B	YRUHQSLDPXNGOKMIEBFZCWVJAT	 	 	 
UKW-C	FVPJIAOYEDRZXWGCTKUQSBNMHL	 	 	 
"""
import warnings
import sys

rotors = ['EKMFLGDQVZNTOWYHXUSPAIBRCJ','AJDKSIRUXBLHWTMCQGZNPYFVOE','BDFHJLCPRTXVZNYEIWGAKMUSQO','ESOVPZJAYQUIRHXLNFTGKDCMWB','VZBRGITYUPSDNHLXAWMJQOFECK']
reflectors = {'A':'EJMZALYXVBWFCRQUONTSPIKHGD', 'B':'YRUHQSLDPXNGOKMIEBFZCWVJAT', 'C':'FVPJIAOYEDRZXWGCTKUQSBNMHL'}
rotorPositions = [1, 1, 1]  # define initial positions of rotors
rotorStack = [1, 2, 3]      # define initial rotors to use in the stack
if (len(rotorPositions) != len(rotorStack)): sys.exit(1)
numRotors = len(rotorStack)

def incrementRotor():
    """Routine to increment the global rotorPositions[] list
    """
    rotorPositions[numRotors - 1] += 1
    for counter in range(numRotors - 1, -1, -1):
        if (rotorPositions[counter] > 26):
            if (counter != 0): rotorPositions[counter - 1] += 1
            rotorPositions[counter] = 1

def rotorReturn(input='A', rotor=1, rotorPos=3):
    """Run a character through a single rotor

    Keyword arguments:
    input -- character to pass through the rotor
    rotor -- the rotor number to run the input through
    rotorPos -- the position of the rotor in the Enigma
    """
    if (rotorPos > numRotors):
        rotorPos = numRotors
        warnings.warn("Resetting rotor position to "+str(rotorPos))
    if (rotor > numRotors): return  # return nothing if we're higher than a valid rotor
    offset = ord('A')
    #print("Sending " + input.upper() + " to rotor " + str(rotor) + " in position " + str(rotorPos))
    return(rotors[rotor-1][ord(input.upper())-offset])

def reflectorReturn(input, reflector='B'):
    """Run a character through the reflector.
  
    Keyword arguments:
    input -- character to pass through the reflector
    reflector - Which UKW version of reflector (valid: B or C, default B)
    """
    if (reflector.upper() not in ['A', 'B', 'C']):
        reflector = "B"
        warnings.warn("Resetting reflector to valid choice")
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
    incrementRotor()
    """ http://www.cryptomuseum.com/crypto/enigma/working.htm
    Below each key of the keyboard is a two-position switch. The key has to be fully depressed before the switch is activated.
    The key also controls the wheel movement. Whenever a key is pressed, the rightmost wheel makes a single step before the
    switch is activated and a lamp is turned on.
    """
    rotorStack.reverse()
    """ reverse() it so you go right-to-left; Enigma signals start on right side of machine """
    counter = numRotors   # track which rotor we're operating on at the moment
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
    return(input)

for c in ['A','F','A']:
    print("Sending " + c + " to Enigma. Output is " + encipherStack(rotorStack, c))
# BUG: If A leads to F, then F should lead to P. It's not. Solve this prior to diving further into rotor incrementing.
        

