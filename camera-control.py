import Quartz
import numpy as np
import cv2

disp_id = Quartz.CGMainDisplayID()

# For OpenCV2 image display
WINDOW_NAME = 'GreenBallTracker'
cv2.ocl.setUseOpenCL(True)


def track(image):

    '''Accepts BGR image as Numpy array
       Returns: (x,y) coordinates of centroid if found
                (-1,-1) if no centroid was found
                None if user hit ESC
    '''

    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image for only green colors
    lower_green = np.array([13,100,150])
    upper_green = np.array([180,255,255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)

    # Assume no centroid
    ctr = (-1,-1)

    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:

        ctr = (centroid_x, centroid_y)
        print(ctr)
        print(centroid_x*2.25, centroid_y*2.5)
        print("\n")
        Quartz.CGDisplayMoveCursorToPoint(disp_id, Quartz.CGPoint(centroid_x*1.5, centroid_y*1.5))


        # Put black circle in at centroid in image
        #cv2.circle(image, ctr, 4, (0,0,0))

    # Display full-color image
    cv2.imshow(WINDOW_NAME, image)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None

    # Return coordinates of centroid
    return ctr

# Test with input from camera
if __name__ == '__main__':
    capture = cv2.VideoCapture(0)
    while True:
        okay, image = capture.read()

        image = cv2.flip(image, 1)
        if okay:
            if not track(image):
                break

            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
           print('Capture failed')
           break
