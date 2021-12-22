
x = 0.002344    # current
y = 0.000950  # bought
z = (x - y) * 100 / x

if z > 0:
    print('+' + str(round(z, 2)) + '%')
else:
    print(str(round(z, 2)) + ' %')
