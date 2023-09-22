s0 = input()
s = ''
a = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'е', 'ё']
state = 0
for i in range(len(s0)):
    if state == 0:
        if s0[i] in a:
            s += s0[i]
        else:
            s += s0[i]
            state = 1
    elif state == 1:
        if s0[i] in a:
            s += s0[i] + 'c' + s0[i]
            state = 0
        else:
            s += s0[i]

print(s)