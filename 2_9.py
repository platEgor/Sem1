s0 = input()
a = ['.', '!', '?']
c = 0
state = 0
for i in range(len(s0)):
    if state == 0:
        if s0[i] in a:
            state = 1
            c += 1
    elif state == 1:
        if not s0[i] in a:
            state = 0
print(c)