#!/usr/bin/python

#Consider binary string "Magic"(TRUE) if 
#1.It starts with the character 1
#2.The string contains at least two 0's.
#3.The string contains an even number of 0's.

import os
import sys

number = raw_input('Enter a number: ')
text = list(number)
#print(text)
count = 0

if text[0] == "1":
    for index,elem in enumerate(text,1):
        #print(index, elem)
        if elem == "0":
            count = count + 1
    #print(count)
    if count >= 2 and count % 2 == 0:
        print("TRUE")
    else:
        print("FALSE")
else:
    print("FALSE")

