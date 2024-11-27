import os 
if not os.path.exists('test.txt'):
    inp = open('test.txt', 'x')
    inp.write('amazing')
else:
    inp = open('test.txt', 'w+')
if os.path.exists('test.txt'):
    inp.write('gryffindor')
inp.close()
out = open('test.txt', '+r')
s = out.read()
print(s)
out.close()
out = open('test.txt', '+w')
out.write('11')
out.close()
out = open('test.txt', '+r')
num = int(out.read())
c = 1
c += num
c = str(c)
out.close()
out = open('test.txt', '+w')
out.write(c)
out.close()


#input.read()
#print(input)