import cv2
from getFaceInfo import *
filePath = "./catch.jpg"


def checkChangeTarget():
    faceInfo = getFaceInfo(filePath)
    leftInfo, rightInfo = getGazeInfo(faceInfo)
    result = isTowards(leftInfo, rightInfo)
    print("Result : ", result)
    return result


if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    count = 0
    check = True
    while True:
        ret, frame = camera.read()
        cv2.imshow("video", frame)
        count += 1
        if count == 60:
            cv2.imwrite(filePath, frame)
            count = 0
            check = checkChangeTarget()
        if check:
            # TODO : send socket to controller
            pass
        if(cv2.waitKey(10) & 0xff == ord('q')):
            break

    camera.release()
    cv2.destroyAllWindows()
    # checkChangeTarget()
