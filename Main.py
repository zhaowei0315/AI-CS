import os
import time
import cv2 as cv
from KeyMouse import shoot
from WindowCapture import WindowCapture
# from YoloV5Detect import detect
# from YoloXDetect import detect
from YoloFastestV2Detect import detect

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

window_name = 'Counter-Strike'

# initialize the WindowCapture class
wincap = WindowCapture(window_name)  # Task Manager
# wincap.list_window_names()

loop_time = time.time()
time.sleep(1)
find_person = False
while True:
    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # debug the loop rate
    fps = 'FPS {}'.format(round(1 / (time.time() - loop_time)))
    loop_time = time.time()

    # detect
    screenshot, output = detect(screenshot)
    if len(output) != 0:
        find_person = True
        # shoot
        (x, y, f) = shoot(output)
        print('敌人坐标：', x, ',', y, ' 置信度：', f)
        cv.putText(screenshot, 'X', (x, y), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))

    # show
    cv.putText(screenshot, fps, (20, 20), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
    cv.imshow(window_name, screenshot)

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
