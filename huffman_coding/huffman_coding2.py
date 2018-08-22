def assign_code(nodes, label, result, prefix = ''):    
    childs = nodes[label]     
    tree = {}
    if len(childs) == 2:
        tree['0'] = assign_code(nodes, childs[0], result, prefix+'0')
        tree['1'] = assign_code(nodes, childs[1], result, prefix+'1')     
        return tree
    else:
        result[label] = prefix
        return label

def huffman_code(_vals):    
    vals = _vals.copy()
    nodes = {}
    for n in vals.keys():
        nodes[n] = []

    while len(vals) > 1:
        s_vals = sorted(vals.items(), key=lambda x:x[1]) 
        a1 = s_vals[0][0]
        a2 = s_vals[1][0]
        vals[a1+a2] = vals.pop(a1) + vals.pop(a2)
        nodes[a1+a2] = [a1, a2]        
    code = {}
    root = a1+a2
    tree = {}
    tree = assign_code(nodes, root, code)
    print(tree)
    print('')
    return code, tree

freq = [
(0.0875, 'e'), (0.05, 'i'), (0.025, 'r'), (0.0125, 'W'), (0.0125, '.'), (0.0125, 'T'), 
(0.1125, 't'), (0.1125, 'w'), (0.125, 'c'), (0.0625, 's'), (0.075, 'a'), (0.1375, ' '), (0.175, 'h')]

vals = {l:v for (v,l) in freq}
code, tree = huffman_code(vals)

text = 'Three witches watch three swatch watches. Which witch watches which swatch watch.' # text to encode
encoded = ''.join([code[tt] for tt in text])
print 'Encoded text:', encoded
print('')

decoded = []
i = 0
while i < len(encoded):
    ch = encoded[i]  
    act = tree[ch]
    while not isinstance(act, str):
        i += 1
        ch = encoded[i]  
        act = act[ch]        
    decoded.append(act)          
    i += 1

print('')
print 'Decoded text:',''.join(decoded)
print('')