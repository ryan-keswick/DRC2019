#
#
#

def output_steering(x):
    letter = 'F'
    
    if x < -350:
        letter = 'K'
    elif x < -250:
        letter = 'J' 
    elif x < -150:
        letter = 'I' 
    elif x < -50:
        letter = 'H'
    elif x < -25:
        letter = 'G'
    elif -25 < x and x < 25:
        letter = 'F'
    elif x > 50:
        letter = 'E'
    elif x > 150:
        letter = 'D' 
    elif x > 250:
        letter = 'C'
    elif x > 350:
        letter = 'B'
    elif x > 400:
        letter = 'A'

    return letter


# Speed ranging from 0..10
# just one for now during testing
def output_speed(percent):
    return '1'

'''
Speed ranges:
0% = 0
10% = 1
…
90% = 9
 there opposite
Turn angles:
0 = A
18 = B
36 = C
54 = D
72 = E
Straight = F
108 = G
126 = H
144 = I
162 = J
180 = K
'''