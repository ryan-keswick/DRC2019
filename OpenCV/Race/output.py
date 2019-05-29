#
#
#

def output_steering(x):
    letter = 'F'
    
    if x < -350:
        letter = 'A'
    elif x < -250:
        letter = 'B' 
    elif x < -150:
        letter = 'C' 
    elif x < -50:
        letter = 'D'
    elif x < -25:
        letter = 'E'
    elif -25 < x and x < 25:
        letter = 'F'
    elif x > 50:
        letter = 'G'
    elif x > 150:
        letter = 'H' 
    elif x > 250:
        letter = 'I'
    elif x > 350:
        letter = 'J'
    elif x > 400:
        letter = 'K'

    return letter


# Speed ranging from 0..10
# just one for now during testing
def output_speed(percent):
    return 1

'''
Speed ranges:
0% = 0
10% = 1
…
90% = 9

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