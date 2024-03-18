from font_analysis import analyze

analyze("CourierPrime-Regular.ttf", 1000)

file = open('save.txt', 'r')
characters = file.read()
file.close()

print(characters)
