import random

scale_int = random.randint(0,100)
amountOfLayers = 0
if (scale_int < 50):
    amountOfLayers = 1
elif (scale_int < 65):
    amountOfLayers = 2
elif (scale_int < 80):
    amountOfLayers = 3
elif (scale_int < 90):
    amountOfLayers = 4

print([random.randint(6,13) for _ in range(10)])
