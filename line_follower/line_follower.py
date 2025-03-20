import GUI
import HAL
import numpy as np
import cv2

prev_error = [0, 0]

Angular_PID = [0.014, 0, 0.001]
Linear_PID = [0.2, 0, 0]
center = [320, 390]

# Enter sequential code!


def pid_control(curr_val, prev_error):
    x_error = curr_val[0] - center[0]
    angular_velocity = Angular_PID[0] * x_error + Angular_PID[2] * (
        x_error - prev_error[0]
    )

    y_error = curr_val[1] - center[1]
    linear_velocity = 3 + (
        Linear_PID[0] * y_error + Linear_PID[2] * (y_error - prev_error[1])
    )
    linear_velocity = np.clip(linear_velocity, 0.5, 3)
    print(angular_velocity)
    print(linear_velocity)
    prev_error = [x_error, y_error]
    return angular_velocity, linear_velocity, prev_error


while True:
    # Enter iterative code!
    image = HAL.getImage()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    res = cv2.bitwise_and(image, image, mask=mask1)

    gray_img = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    _, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
    # _, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    moments = cv2.moments(binary_img)
    # height, width = binary_img.shape

    # print(f"Resolution: {width} x {height}")

    centroid = (moments["m10"] / moments["m00"], moments["m01"] / moments["m00"])
    print(f"centroid : {centroid}")
    angular_velocity, linear_velocity, prev_error = pid_control(centroid, prev_error)

    HAL.setV(linear_velocity)
    HAL.setW(-angular_velocity)

    cv2.circle(binary_img, (int(centroid[0]), int(centroid[1])), 5, (0, 255, 0), 2)
    # Print some moment values
    print(f"m00 (Area): {moments['m00']}")
    print(f"m10: {moments['m10']}, m01: {moments['m01']}")

    GUI.showImage(binary_img)
