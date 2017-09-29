f = open('1.txt').read()
numbers = f.split(',')
res = []

q = []
for number in numbers:
    q.append(int(number))

counter = 1
while counter < 580:
    if counter in q:
        q.remove(counter)
        res.append(counter)
    else:
        res.append('XXX')
    counter += 1
# print(len(res))
# print(res[570:])

company = "google"
f = open('%s_raw.txt' % company, 'w+')
f.write(str(res))
f.close()