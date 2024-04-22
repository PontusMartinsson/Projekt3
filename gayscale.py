import cv2

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

ye = "MQW@N$gEBHmKqpRX#kdA&b%GSDwhPF8ZOUTxa69se0yVYnf4z2CL5u3JojcvItrli17/?*=+!~,-."

yelen = len(ye)-1

image = cv2.imread('.\img\KORV_128x64.png', cv2.IMREAD_GRAYSCALE)

i = 0
while i < len(image):
    output=""
    j = 0
    while j < len(image[i]):
        num = translate(image[i][j], 0, 255, 0, yelen)
        output = output + ye[num]
        j += 1

    print(output)
    i += 1
