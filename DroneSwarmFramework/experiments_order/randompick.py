# we have 4 different types of analysis :
# 1 : Controller : FPS
# 2 : Controller : Fixed
# 3 : MOCAP : FPS
# 4 : MOCAP : Fixed


import math
import numpy as np
import random

numb = 4
possibilities = math.factorial(numb)

list = []
curr_run = ''
digits = []

while len(list) < possibilities:
   curr_digit = random.randint(1,numb)
   if curr_digit not in digits:
      digits.append(curr_digit)
      if len(digits) == numb:
         for temp in digits:
            curr_run += str(temp)
         if curr_run not in list:
            list.append(curr_run)
            curr_run = ''
            digits = []
         else:
            curr_run = ''
            digits = []

for idx,i in enumerate(list):
   print(idx, 'th run', i)
