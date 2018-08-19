#!/usr/bin/env python

__author__ = "Dzvezdana Arsovska"

from time import sleep
print ('PROGRAM START\n')

def make_leaf(symbol,weight):
    return(symbol,weight)

def is_leaf(x):
    return isinstance(x,tuple) and \
    len(x)==2 and \
    isinstance(x[0],str) and \
    isinstance(x[1],float)

def get_leaf_symbol(x):
    return x[0]

def get_leaf_freq(x):
    return x[1]

def get_left_branch(tree):
    return tree[0]

def get_right_branch(tree):
    return tree[1]

def get_symbols(tree):
    if is_leaf(tree):
        return [get_leaf_symbol(tree)]
    else:
        return tree[2]
    
def get_freq(tree):
    if is_leaf(tree):
        return get_leaf_freq(tree)
    else:
        return tree[3]

def make_tree(L_b,R_b):
    return [L_b,
            R_b,
            get_symbols(L_b)+get_symbols(R_b),
            get_freq(L_b)+get_freq(R_b)]

# PART 1

#LEFT TREE
L_tree1=make_tree(make_leaf('W',0.0125),
                          make_tree(make_leaf('.',0.0125),make_leaf('T',0.0125)))

L_tree2=make_tree(make_leaf('r',0.025),L_tree1)
L_tree3=make_tree(make_leaf('i',0.05),L_tree2)
L_tree4=make_tree(make_leaf('e',0.0875),L_tree3)

L_tree5=make_tree(make_leaf('t',0.1125),make_leaf('w',0.1125))
L_tree6=make_tree(L_tree4,L_tree5)

#RIGHT TREE
R_tree1=make_tree(make_leaf('c',0.125),
                          make_tree(make_leaf('s',0.0625),make_leaf('a',0.075)))
R_tree2=make_tree(make_leaf(' ',0.1375),make_leaf('h',0.175))
R_tree3=make_tree(R_tree1,R_tree2)

#TREE MERGED
F_tree=make_tree(L_tree6,R_tree3)
print (F_tree)
print('')

#PART 2

#encoding
def huffman_encode_symbol(s,tree):
    encoding = []
    stringi=""
    c_branch = tree

    while not is_leaf(c_branch):
        if not s in get_symbols(c_branch):
            return 'error 1'
        elif s in get_symbols(get_left_branch(c_branch)):
            encoding.append('0')
            
            c_branch=get_left_branch(c_branch)
        elif s in get_symbols(get_right_branch(c_branch)):
            encoding.append('1')
            
            c_branch=get_right_branch(c_branch)
        else:
            return 'error 2'
     
    return encoding

def huffman_encode(sym,tree):
    encoding=[]
    
    for s in sym:
        encoding.extend(huffman_encode_symbol(s,tree)) #extend is list extension
    return encoding

def huffman_decode(data,tree):
    sim=get_symbols(tree) 
    k=len(sim)
    #print(sim)
    seq=''
    result=''

    for bit in data:
        seq=seq+bit
        i=0
        #print(seq)
        while (i<k):
            h=huffman_encode(sim[i],F_tree)
            if seq == (''.join((h))):
                       result=result+sim[i]
                       seq=''
            i=i+1
            #print(i)
    print('Decoded message:')
    print(result)
    
bits='001111111100110000000110011001001010011100010101100111011010100111110010111001100000001101010011101101010011111001110110101001110001010001111011000111011100101001111100110010010100111110011101101010011100010101100111110010100111110101001110110101001111100111011010100111'
o=huffman_decode(bits,F_tree)

#Checking if the result is the same as the original by encoding
print('')
print('')
print('')
print('CHECK RESULT:')
print('')

proba=huffman_encode('Three witches watch three swatch watches. Which witch watches which swatch watch',F_tree)

res=''.join((proba))
original='001111111100110000000110011001001010011100010101100111011010100111110010111001100000001101010011101101010011111001110110101001110001010001111011000111011100101001111100110010010100111110011101101010011100010101100111110010100111110101001110110101001111100111011010100111'
if res==original:
    print('CHECK CONFIRMED')
else:
    print('CHECK FAILED')

'''
#decoding
def huffman_decode(data, tree):
  
    # get the bit value
    # start from root and go down the tree
    # if the bit is 0 go left
    # if the bit is 1 go right
    # go down the tree till a leaf is found
    # get the leaf symbol and to decode next symbol repeat the process
    #decoding = []
    #return decoding
'''
