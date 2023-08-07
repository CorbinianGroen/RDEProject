#global s
#s = 'hello'

global m
m = 'huhu'

print(globals())

if 's' in globals():
    print('s in globals')

if 's' not in globals() and 'm' in globals():
    print('s not in globals')