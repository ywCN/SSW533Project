f = open('1.txt').read()
numbers = f.split(',')
res = []

q = []
print(type(q))
print(type(numbers[0]))
print(type(int(numbers[0])))
for number in numbers:
    q.append(int(number))

print(len(q))
counter = 1
while counter < 600:
    if counter in q:
        q.remove(counter)
        res.append(counter)
    else:
        counter += 1
        res.append('XXX')

print(res)
