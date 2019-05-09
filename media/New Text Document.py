def chan(a):
    if a % 2 == 0:
        return True
    else:
        return False
        
# a = input()
a = '127'
sc = 0 
sl = 0
for i in a:
    if chan(int(i)):
        sc += int(i)
    sl += int(i)

if sl % sc == 0:
    print('YES')
else:
    print('NO')