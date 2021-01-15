import cv2
import numpy as np

# Reading Image and converting it to gray scale.
img = cv2.imread('Hough.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
width = img.shape[1]

# Creating output images and files.
red_lines = img.copy()
blue_lines = img.copy()
coin = img.copy()
red_lines_file = "results/red_lines.txt"
blue_lines_file = "results/blue_lines.txt"
coin_file = "results/coins.txt"

with open(red_lines_file, "w") as file:
    file.write("")
with open(blue_lines_file, "w") as file:
    file.write("")
with open(coin_file, "w") as file:
    file.write("")

# Threshold and Bluring
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                               cv2.THRESH_BINARY, 7, 7)

# Detecting Edges and Lines.
edges = cv2.Canny(thresh, 75, 100, apertureSize=5)
lines = cv2.HoughLines(edges, 1, np.pi / 90, 150, np.array([]), 1)


# Function to differentiate and draw lines.
def sort_lines(line):
    for [[rho, theta]] in line:
        if theta != 0:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            if theta > 2.7:
                cv2.line(red_lines, (x1, y1), (x2, y2), (0, 0, 255), 4)
                '''
                Transforming the co-ordinate to the one given in the question. 
                The same can be acheived by cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                in the start after loading the image
                '''
                theta = round(theta * 180 / np.pi) - 90
                rho = -rho
                with open(red_lines_file, "a") as file:
                    file.write("[" + str(theta) + "," + str(rho) + "]\n")
            else:
                cv2.line(blue_lines, (x1, y1), (x2, y2), (255, 0, 0), 4)
                '''
                Transforming the co-ordinate to the one given in the question. 
                The same can be acheived by cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
                in the start after loading the image
                '''
                theta = round(theta * 180 / np.pi) - 90
                rho = -rho
                with open(blue_lines_file, "a") as file:
                    file.write("[" + str(theta) + "," + str(rho) + "]\n")


# Code to remove multiple lines.
n2 = 0
strong_lines = np.zeros([15, 1, 2])
for n1 in range(0, len(lines)):
    for rho, theta in lines[n1]:
        if n1 == 0:
            strong_lines[n2] = lines[n1]
            n2 = n2 + 1
        else:
            closeness_rho = np.isclose(rho, strong_lines[0:n2, 0, 0], atol=20)
            closeness_theta = np.isclose(theta, strong_lines[0:n2, 0, 1], atol=np.pi / 90)
            closeness = np.all([closeness_rho, closeness_theta], axis=0)
            if not any(closeness) and n2 < 15:
                strong_lines[n2] = lines[n1]
                n2 = n2 + 1

sort_lines(strong_lines)

# Detect circles in the image
circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, 43,
                           param1=100,
                           param2=17,
                           minRadius=10,
                           maxRadius=40)

# Draw Circles
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circles:
        cv2.rectangle(coin, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        cv2.circle(coin, (x, y), r, (0, 255, 0), 4)
        with open(coin_file, "a") as file:
            file.write("["+str(y)+","+str(width-x)+","+str(r)+"]\n")

cv2.imwrite('results/coins.jpg', coin)
cv2.imwrite('results/red_lines.jpg', red_lines)
cv2.imwrite('results/blue_lines.jpg', blue_lines)

