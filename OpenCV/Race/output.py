#
#
#

def output_steering(x):

    letter = 'F'
    if -350 > x:
       letter = 'K'   
    elif -350 < x and x < -300:
       letter = 'K'   
    elif -300 < x and x < -250:
       letter = 'J'   
    elif -250 < x and x < -100:
       letter = 'I'   
    elif -100 < x and x < -10:
       letter = 'H'   
    elif -10 < x and x < 10:
       letter = 'F'   
    elif 10 < x and x < 100:
       letter = 'D'   
    elif 100 < x and x < 250:
       letter = 'C'   
    elif 250 < x and x < 299:
       letter = 'B'   
    elif 300 < x and x < 350:
       letter = 'A'   
    elif x > 350:
       letter = 'A'   




    return letter


# Speed ranging from 0..10
# just one for now during testing
def output_speed(steer):
   if -100 < steer and steer < 100:
      return '4'
   return '2'

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