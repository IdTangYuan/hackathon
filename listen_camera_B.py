import cv2
import socket
from getFaceInfo import *
filePath = "./catch.jpg"
host = "10.64.83.12"
port = 5052


def checkChangeTarget():
    try:
        faceInfo = getFaceInfo(filePath)
        if (json.loads(faceInfo)['faces'].__len__() == 0):
            return False
        leftInfo, rightInfo = getGazeInfo(faceInfo)
        result = isTowards(leftInfo, rightInfo)
        print("Result : ", result)
        return result
    except Exception as e:
        raise
    else:
        return False


if __name__ == '__main__':
    s = socket.socket()
    s.connect((host, port))
    camera = cv2.VideoCapture(0)
    count = 0
    check = True
    while True:
        ret, frame = camera.read()
        cv2.imshow("video", frame)
        count += 1
        if count == 30:
            cv2.imwrite(filePath, frame)
            count = 0
            check = checkChangeTarget()
            if check:
                s.send(b"True")

        if(cv2.waitKey(10) & 0xff == ord('q')):
            break

    s.close()
    camera.release()
    cv2.destroyAllWindows()
    # checkChangeTarget()