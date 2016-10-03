str = raw_input('Input a string:')
digit = 0
alpha = 0
space = 0
others = 0

for s in str:
    if s.isalpha():
        alpha += 1
    elif s.isdigit():
        digit += 1
    elif s.isspace():
        space += 1
    else:
        others += 1

print alpha, 'alphas;', digit, 'digit;', space, 'space;', others, 'others left.'
