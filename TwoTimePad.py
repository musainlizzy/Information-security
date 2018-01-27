#!/usr/bin/env python 
import string
import collections

# many-time pad attack:https://github.com/Jwomers/many-time-pad-attack/blob/master/attack.py
def strxor(a, b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

c1 = '7f4d115b59511a4d5f585418435550155d4311475d1840515645415d19101314'
c2 = '5f555f4d17585e525315584c135641411444595d41185c5a50105a4b55585c50'
c3 = '54515458441443515315435d404451564010465c5b5b5b145c43135c4d54465a'
c4 = "5c5b11585e595e4d16415e18445c55411451115953561357545e135c57115d47"
c5 = "6b5b44145a41444d16575418475c51155758505a555d134d5a45134f51425a15"
c6 = "665c5847175d44195715455d4040145a5210455c571876595042545d56524b15"
c7 = "665c5e414455595d45155e5e1357555b505c5447125b525a1552565451565a41"
c8 = "7b52485b42145b564050114c5b5b47501447595b12545c4250105c4c50544046"
ciphers = [c1, c2, c3, c4, c5, c6, c7,c8]

target = c6

final_key = [None]*len(c1)
known_key_positions = set()

for current_index, ciphertext in enumerate(ciphers):
    counter = collections.Counter()
    for index, ciphertext2 in enumerate(ciphers):
        if current_index != index: # don't xor a ciphertext with itself
            for indexOfChar, char in enumerate(strxor(ciphertext.decode('hex'), ciphertext2.decode('hex'))): # Xor the two ciphertexts
                if char in string.printable and char.isalpha(): counter[indexOfChar] += 1 # Increment the counter at this index
    knownSpaceIndexes = []

    for ind, val in counter.items():
        if val >= 5: knownSpaceIndexes.append(ind)


    xor_with_spaces = strxor(ciphertext.decode('hex'),' '*len(c1))
    for index in knownSpaceIndexes:
        final_key[index] = xor_with_spaces[index].encode('hex')
        known_key_positions.add(index)


final_key_hex = ''.join([val if val is not None else '00' for val in final_key])
output = strxor(target.decode('hex'),final_key_hex.decode('hex'))
print ''.join([char if index in known_key_positions else '*' for index, char in enumerate(output)])
testKey=strxor(target.decode('hex'), "This is a test of the Emergency ")
print testKey
print strxor(c1.decode('hex'),testKey)
print strxor(c2.decode('hex'),testKey)
print strxor(c3.decode('hex'),testKey)
print strxor(c4.decode('hex'),testKey)
print strxor(c5.decode('hex'),testKey)
print strxor(c6.decode('hex'),testKey)
print strxor(c7.decode('hex'),testKey)
print strxor(c8.decode('hex'),testKey)






