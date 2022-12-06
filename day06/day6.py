with open('input.txt') as f:
    code = f.read()
    found4 = found14 = False
    for i in range(0,len(code)-4):
        if not found4 and len(set(code[i:i+4])) == 4:
            print('{} @ {}'.format(code[i:i+4],i+4))
            found4 = True
        if not found14 and len(set(code[i:i+14])) == 14:
            print('{} @ {}'.format(code[i:i+14],i+14))
            found14 = True