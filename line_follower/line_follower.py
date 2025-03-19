import GUI
import HAL
import numpy as np
import cv2


# Enter sequential code!
def moment_calc():
    return 0


def pid_control():
    return 0

def check_img_prop(img):
    height, width, channels = img.shape

    print(f"Resolution: {width} x {height}")
    print(f"Number of Channels: {channels}")

while True:
    # Enter iterative code!
    image = HAL.getImage()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])

    HAL.setV(5)
    # HAL.setW(10)
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    res = cv2.bitwise_and(image, image, mask=mask1)

    gray_img = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    _,binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
    #_, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    moments = cv2.moments(binary_img)
    #height, width = binary_img.shape

    #print(f"Resolution: {width} x {height}")
    
    centroid = (moments['m10']/moments['m00'], moments['m01']/moments['m00'])
    print(f"centroid : {centroid}")
    cv2.circle(binary_img, centroid , 5, (0, 255, 0), 2)
    # Print some moment values
    print(f"m00 (Area): {moments['m00']}")
    print(f"m10: {moments['m10']}, m01: {moments['m01']}")

    GUI.showImage(binary_img)
