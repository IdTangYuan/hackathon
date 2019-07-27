# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import time
import json


def getFaceInfo(filePath):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    key = "31lP9U1TGbS9l5iqZYvgTGPOD6P8Gwnx"
    secret = "ECkq3pfhq9qf7SGz-LrwKoupmIiPh7Gc"
    #filepath = r"C://Users/tangre/TRH/code/hackathon/2.jpg"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    fr = open(filePath, 'rb')
    data.append(
        'Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(fr.read())
    fr.close()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' %
                'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' %
                'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header(
        'Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=5)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        # print(qrcont.decode('utf-8'))
        return qrcont.decode('utf-8')
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))
        return False

# paras gaze data from FaceInfo(JSON)
# faces[]{} -> attributes{} -> eyegaze{} -> right_eye_gaze{} -> vector_z_component, vector_x_component, vector_y_component
#                                       -> left_eye_gaze{}  -> vector_z_component, vector_x_component, vector_y_component


def getGazeInfo(FaceInfo):
    data = json.loads(FaceInfo)
    rightEyeGaze = data['faces'][0]['attributes']['eyegaze']['right_eye_gaze']
    leftEyeGaze = data['faces'][0]['attributes']['eyegaze']['left_eye_gaze']
    rightInfo = {'x': rightEyeGaze['vector_x_component'],
                 'y': rightEyeGaze['vector_y_component'], 'z': rightEyeGaze['vector_z_component']}
    leftInfo = {'x': leftEyeGaze['vector_x_component'],
                'y': leftEyeGaze['vector_y_component'], 'z': leftEyeGaze['vector_z_component']}
    # print("right eye gaze :", rightInfo)
    # print("left eye gaze :", leftInfo)
    return leftInfo, rightInfo


def isTowards(leftInfo, rightInfo):
    threshold = 0.8
    leftAngle = getAngle3D(leftInfo)
    rightAngle = getAngle3D(rightInfo)
    # print("left Angle Tangent2 : ", leftAngle)
    # print("right Angle Tangent2 : ", rightAngle)
    if(leftAngle < threshold and rightAngle < threshold):
        return True
    else:
        return False


def getAngle3D(vector):
    def square(x):
        return x * x
    tan2 = (square(vector['x']) + square(vector['y'])) / square(vector['z'])
    return tan2


if __name__ == '__main__':
    FaceInfoCorrect = """
{
    "time_used":  1498,
     "faces":  [
        {
            "landmark":  {
                "mouth_upper_lip_left_contour2":  {
                    "y":  1769,
                     "x":  1393
                },
                 "mouth_upper_lip_top":  {
                    "y":  1746,
                     "x":  1531
                },
                 "mouth_upper_lip_left_contour1":  {
                    "y":  1730,
                     "x":  1479
                },
                 "left_eye_upper_left_quarter":  {
                    "y":  1207,
                     "x":  1209
                },
                 "left_eyebrow_lower_middle":  {
                    "y":  1047,
                     "x":  1260
                },
                 "mouth_upper_lip_left_contour3":  {
                    "y":  1816,
                     "x":  1425
                },
                 "right_eye_top":  {
                    "y":  1216,
                     "x":  1792
                },
                 "left_eye_bottom":  {
                    "y":  1261,
                     "x":  1262
                },
                 "right_eyebrow_lower_left_quarter":  {
                    "y":  1045,
                     "x":  1729
                },
                 "right_eye_pupil":  {
                    "y":  1249,
                     "x":  1778
                },
                 "mouth_lower_lip_right_contour1":  {
                    "y":  1830,
                     "x":  1602
                },
                 "mouth_lower_lip_right_contour3":  {
                    "y":  1910,
                     "x":  1585
                },
                 "mouth_lower_lip_right_contour2":  {
                    "y":  1881,
                     "x":  1636
                },
                 "contour_chin":  {
                    "y":  2150,
                     "x":  1495
                },
                 "contour_left9":  {
                    "y":  2125,
                     "x":  1342
                },
                 "left_eye_lower_right_quarter":  {
                    "y":  1254,
                     "x":  1318
                },
                 "mouth_lower_lip_top":  {
                    "y":  1828,
                     "x":  1523
                },
                 "right_eyebrow_upper_middle":  {
                    "y":  972,
                     "x":  1825
                },
                 "left_eyebrow_left_corner":  {
                    "y":  1076,
                     "x":  1065
                },
                 "right_eye_bottom":  {
                    "y":  1292,
                     "x":  1787
                },
                 "contour_left7":  {
                    "y":  1970,
                     "x":  1106
                },
                 "contour_left6":  {
                    "y":  1864,
                     "x":  1023
                },
                 "contour_left5":  {
                    "y":  1744,
                     "x":  966
                },
                 "contour_left4":  {
                    "y":  1614,
                     "x":  935
                },
                 "contour_left3":  {
                    "y":  1481,
                     "x":  918
                },
                 "contour_left2":  {
                    "y":  1349,
                     "x":  914
                },
                 "contour_left1":  {
                    "y":  1217,
                     "x":  925
                },
                 "left_eye_lower_left_quarter":  {
                    "y":  1251,
                     "x":  1208
                },
                 "contour_right1":  {
                    "y":  1287,
                     "x":  2024
                },
                 "contour_right3":  {
                    "y":  1526,
                     "x":  1997
                },
                 "contour_right2":  {
                    "y":  1408,
                     "x":  2018
                },
                 "mouth_left_corner":  {
                    "y":  1828,
                     "x":  1320
                },
                 "contour_right4":  {
                    "y":  1643,
                     "x":  1965
                },
                 "contour_right7":  {
                    "y":  1963,
                     "x":  1810
                },
                 "right_eyebrow_left_corner":  {
                    "y":  1025,
                     "x":  1647
                },
                 "nose_right":  {
                    "y":  1580,
                     "x":  1685
                },
                 "nose_tip":  {
                    "y":  1481,
                     "x":  1547
                },
                 "contour_right5":  {
                    "y":  1757,
                     "x":  1928
                },
                 "nose_contour_lower_middle":  {
                    "y":  1620,
                     "x":  1534
                },
                 "left_eyebrow_lower_left_quarter":  {
                    "y":  1062,
                     "x":  1161
                },
                 "mouth_lower_lip_left_contour3":  {
                    "y":  1905,
                     "x":  1437
                },
                 "right_eye_right_corner":  {
                    "y":  1270,
                     "x":  1881
                },
                 "right_eye_lower_right_quarter":  {
                    "y":  1287,
                     "x":  1839
                },
                 "mouth_upper_lip_right_contour2":  {
                    "y":  1779,
                     "x":  1642
                },
                 "right_eyebrow_lower_right_quarter":  {
                    "y":  1069,
                     "x":  1885
                },
                 "left_eye_left_corner":  {
                    "y":  1228,
                     "x":  1164
                },
                 "mouth_right_corner":  {
                    "y":  1844,
                     "x":  1676
                },
                 "mouth_upper_lip_right_contour3":  {
                    "y":  1824,
                     "x":  1604
                },
                 "right_eye_lower_left_quarter":  {
                    "y":  1278,
                     "x":  1734
                },
                 "left_eyebrow_right_corner":  {
                    "y":  1028,
                     "x":  1460
                },
                 "left_eyebrow_lower_right_quarter":  {
                    "y":  1040,
                     "x":  1362
                },
                 "right_eye_center":  {
                    "y":  1259,
                     "x":  1787
                },
                 "nose_left":  {
                    "y":  1566,
                     "x":  1365
                },
                 "mouth_lower_lip_left_contour1":  {
                    "y":  1822,
                     "x":  1425
                },
                 "left_eye_upper_right_quarter":  {
                    "y":  1208,
                     "x":  1321
                },
                 "right_eyebrow_lower_middle":  {
                    "y":  1053,
                     "x":  1812
                },
                 "left_eye_top":  {
                    "y":  1199,
                     "x":  1262
                },
                 "left_eye_center":  {
                    "y":  1232,
                     "x":  1264
                },
                 "contour_left8":  {
                    "y":  2059,
                     "x":  1213
                },
                 "contour_right9":  {
                    "y":  2121,
                     "x":  1627
                },
                 "right_eye_left_corner":  {
                    "y":  1259,
                     "x":  1690
                },
                 "mouth_lower_lip_bottom":  {
                    "y":  1920,
                     "x":  1517
                },
                 "left_eyebrow_upper_left_quarter":  {
                    "y":  995,
                     "x":  1142
                },
                 "left_eye_pupil":  {
                    "y":  1229,
                     "x":  1273
                },
                 "right_eyebrow_upper_left_quarter":  {
                    "y":  971,
                     "x":  1727
                },
                 "contour_right8":  {
                    "y":  2051,
                     "x":  1728
                },
                 "right_eyebrow_right_corner":  {
                    "y":  1089,
                     "x":  1950
                },
                 "right_eye_upper_left_quarter":  {
                    "y":  1224,
                     "x":  1734
                },
                 "left_eyebrow_upper_middle":  {
                    "y":  960,
                     "x":  1252
                },
                 "right_eyebrow_upper_right_quarter":  {
                    "y":  1009,
                     "x":  1905
                },
                 "nose_contour_left1":  {
                    "y":  1244,
                     "x":  1446
                },
                 "nose_contour_left2":  {
                    "y":  1468,
                     "x":  1401
                },
                 "mouth_upper_lip_right_contour1":  {
                    "y":  1735,
                     "x":  1583
                },
                 "nose_contour_right1":  {
                    "y":  1259,
                     "x":  1625
                },
                 "nose_contour_right2":  {
                    "y":  1479,
                     "x":  1662
                },
                 "mouth_lower_lip_left_contour2":  {
                    "y":  1871,
                     "x":  1374
                },
                 "contour_right6":  {
                    "y":  1865,
                     "x":  1876
                },
                 "nose_contour_right3":  {
                    "y":  1603,
                     "x":  1613
                },
                 "nose_contour_left3":  {
                    "y":  1598,
                     "x":  1446
                },
                 "left_eye_right_corner":  {
                    "y":  1240,
                     "x":  1369
                },
                 "left_eyebrow_upper_right_quarter":  {
                    "y":  967,
                     "x":  1372
                },
                 "right_eye_upper_right_quarter":  {
                    "y":  1235,
                     "x":  1845
                },
                 "mouth_upper_lip_bottom":  {
                    "y":  1818,
                     "x":  1525
                }
            },
             "attributes":  {
                "emotion":  {
                    "sadness":  64.353,
                     "neutral":  35.145,
                     "disgust":  0.068,
                     "anger":  0.053,
                     "surprise":  0.119,
                     "fear":  0.246,
                     "happiness":  0.018
                },
                 "beauty":  {
                    "female_score":  69.91,
                     "male_score":  72.152
                },
                 "gender":  {
                    "value":  "Male"
                },
                 "age":  {
                    "value":  22
                },
                 "mouthstatus":  {
                    "close":  99.998,
                     "surgical_mask_or_respirator":  0.0,
                     "open":  0.002,
                     "other_occlusion":  0.0
                },
                 "glass":  {
                    "value":  "Normal"
                },
                 "skinstatus":  {
                    "dark_circle":  6.76,
                     "stain":  6.393,
                     "acne":  7.706,
                     "health":  34.672
                },
                 "headpose":  {
                    "yaw_angle":  -4.428965,
                     "pitch_angle":  -1.4596105,
                     "roll_angle":  3.8078806
                },
                 "blur":  {
                    "blurness":  {
                        "threshold":  50.0,
                         "value":  0.36
                    },
                     "motionblur":  {
                        "threshold":  50.0,
                         "value":  0.36
                    },
                     "gaussianblur":  {
                        "threshold":  50.0,
                         "value":  0.36
                    }
                },
                 "smile":  {
                    "threshold":  50.0,
                     "value":  0.068
                },
                 "eyestatus":  {
                    "left_eye_status":  {
                        "normal_glass_eye_open":  99.899,
                         "no_glass_eye_close":  0.0,
                         "occlusion":  0.026,
                         "no_glass_eye_open":  0.01,
                         "normal_glass_eye_close":  0.047,
                         "dark_glasses":  0.018
                    },
                     "right_eye_status":  {
                        "normal_glass_eye_open":  99.992,
                         "no_glass_eye_close":  0.0,
                         "occlusion":  0.0,
                         "no_glass_eye_open":  0.008,
                         "normal_glass_eye_close":  0.0,
                         "dark_glasses":  0.0
                    }
                },
                 "facequality":  {
                    "threshold":  70.1,
                     "value":  91.81
                },
                 "ethnicity":  {
                    "value":  "ASIAN"
                },
                 "eyegaze":  {
                    "right_eye_gaze":  {
                        "position_x_coordinate":  0.452,
                         "vector_z_component":  0.981,
                         "vector_x_component":  -0.154,
                         "vector_y_component":  0.116,
                         "position_y_coordinate":  0.445
                    },
                     "left_eye_gaze":  {
                        "position_x_coordinate":  0.513,
                         "vector_z_component":  0.972,
                         "vector_x_component":  0.117,
                         "vector_y_component":  0.202,
                         "position_y_coordinate":  0.482
                    }
                }
            },
             "face_rectangle":  {
                "width":  1190,
                 "top":  957,
                 "left":  864,
                 "height":  1190
            },
             "face_token":  "1e32c4148142db24700a5150b5dc34da"
        }
    ],
     "image_id":  "tulVKeGAsSeI8+pFzTfb7g==",
     "request_id":  "1564128023,7aaa7903-02f0-4f57-ba09-876116d88ec5",
     "face_num":  1
}

    """
    FaceInfoFalse = """
    {
    "time_used":  1530,
     "faces":  
    [
        
        {
            
            "landmark":  {
                
                "mouth_upper_lip_left_contour2":  {
                    
                    "y":  1661,
                     
                    "x":  1349
                
                },
                 
                "mouth_upper_lip_top":  {
                    
                    "y":  1654,
                     
                    "x":  1463
                
                },
                 
                "mouth_upper_lip_left_contour1":  {
                    
                    "y":  1639,
                     
                    "x":  1428
                
                },
                 
                "left_eye_upper_left_quarter":  {
                    
                    "y":  1114,
                     
                    "x":  1231
                
                },
                 
                "left_eyebrow_lower_middle":  {
                    
                    "y":  965,
                     
                    "x":  1287
                
                },
                 
                "mouth_upper_lip_left_contour3":  {
                    
                    "y":  1696,
                     
                    "x":  1369
                
                },
                 
                "right_eye_top":  {
                    
                    "y":  1228,
                     
                    "x":  1562
                
                },
                 
                "left_eye_bottom":  {
                    
                    "y":  1166,
                     
                    "x":  1261
                
                },
                 
                "right_eyebrow_lower_left_quarter":  {
                    
                    "y":  1084,
                     
                    "x":  1559
                
                },
                 
                "right_eye_pupil":  {
                    
                    "y":  1238,
                    
                    "x":  1554
                
                },
                 
                "mouth_lower_lip_right_contour1":  {
                    "y":  1735,
                     "x":  1485
                },
                 "mouth_lower_lip_right_contour3":  {
                    "y":  1789,
                     "x":  1473
                },
                 "mouth_lower_lip_right_contour2":  {
                    "y":  1772,
                     "x":  1501
                },
                 "contour_chin":  {
                    "y":  2053,
                     "x":  1358
                },
                 "contour_left9":  {
                    "y":  2057,
                     "x":  1196
                },
                 "left_eye_lower_right_quarter":  {
                    "y":  1172,
                     "x":  1304
                },
                 "mouth_lower_lip_top":  {
                    "y":  1727,
                     "x":  1444
                },
                 "right_eyebrow_upper_middle":  {
                    "y":  1059,
                     "x":  1598
                },
                 "left_eyebrow_left_corner":  {
                    "y":  936,
                     "x":  1123
                },
                 "right_eye_bottom":  {
                    "y":  1251,
                     "x":  1552
                },
                 "contour_left7":  {
                    "y":  1945,
                     "x":  878
                },
                 "contour_left6":  {
                    "y":  1848,
                     "x":  747
                },
                 "contour_left5":  {
                    "y":  1722,
                     "x":  655
                },
                 "contour_left4":  {
                    "y":  1570,
                     "x":  610
                },
                 "contour_left3":  {
                    "y":  1410,
                     "x":  603
                },
                 "contour_left2":  {
                    "y":  1253,
                     "x":  616
                },
                 "contour_left1":  {
                    "y":  1102,
                     "x":  644
                },
                 "left_eye_lower_left_quarter":  {
                    "y":  1148,
                     "x":  1221
                },
                 "contour_right1":  {
                    "y":  1248,
                     "x":  1608
                },
                 "contour_right3":  {
                    "y":  1433,
                     "x":  1612
                },
                 "contour_right2":  {
                    "y":  1338,
                     "x":  1610
                },
                 "mouth_left_corner":  {
                    "y":  1705,
                     "x":  1277
                },
                 "contour_right4":  {
                    "y":  1531,
                     "x":  1604
                },
                 "contour_right7":  {
                    "y":  1815,
                     "x":  1522
                },
                 "right_eyebrow_left_corner":  {
                    "y":  1077,
                     "x":  1531
                },
                 "nose_right":  {
                    "y":  1513,
                     "x":  1557
                },
                 "nose_tip":  {
                    "y":  1426,
                     "x":  1547
                },
                 "contour_right5":  {
                    "y":  1630,
                     "x":  1587
                },
                 "nose_contour_lower_middle":  {
                    "y":  1539,
                     "x":  1474
                },
                 "left_eyebrow_lower_left_quarter":  {
                    "y":  950,
                     "x":  1204
                },
                 "mouth_lower_lip_left_contour3":  {
                    "y":  1772,
                     "x":  1374
                },
                 "right_eye_right_corner":  {
                    "y":  1258,
                     "x":  1591
                },
                 "right_eye_lower_right_quarter":  {
                    "y":  1258,
                     "x":  1572
                },
                 "mouth_upper_lip_right_contour2":  {
                    "y":  1697,
                     "x":  1525
                },
                 "right_eyebrow_lower_right_quarter":  {
                    "y":  1093,
                     "x":  1615
                },
                 "left_eye_left_corner":  {
                    "y":  1120,
                     "x":  1191
                },
                 "mouth_right_corner":  {
                    "y":  1750,
                     "x":  1518
                },
                 "mouth_upper_lip_right_contour3":  {
                    "y":  1721,
                     "x":  1491
                },
                 "right_eye_lower_left_quarter":  {
                    "y":  1239,
                     "x":  1534
                },
                 "left_eyebrow_right_corner":  {
                    "y":  1002,
                     "x":  1453
                },
                 "left_eyebrow_lower_right_quarter":  {
                    "y":  987,
                     "x":  1369
                },
                 "right_eye_center":  {
                    "y":  1241,
                     "x":  1556
                },
                 "nose_left":  {
                    "y":  1487,
                     "x":  1328
                },
                 "mouth_lower_lip_left_contour1":  {
                    "y":  1713,
                     "x":  1367
                },
                 "left_eye_upper_right_quarter":  {
                    "y":  1136,
                     "x":  1317
                },
                 "right_eyebrow_lower_middle":  {
                    "y":  1089,
                     "x":  1586
                },
                 "left_eye_top":  {
                    "y":  1119,
                     "x":  1275
                },
                 "left_eye_center":  {
                    "y":  1143,
                     "x":  1268
                },
                 "contour_left8":  {
                    "y":  2015,
                     "x":  1031
                },
                 "contour_right9":  {
                    "y":  1987,
                     "x":  1432
                },
                 "right_eye_left_corner":  {
                    "y":  1226,
                     "x":  1518
                },
                 "mouth_lower_lip_bottom":  {
                    "y":  1791,
                     "x":  1433
                },
                 "left_eyebrow_upper_left_quarter":  {
                    "y":  891,
                     "x":  1209
                },
                 "left_eye_pupil":  {
                    "y":  1147,
                     "x":  1286
                },
                 "right_eyebrow_upper_left_quarter":  {
                    "y":  1061,
                     "x":  1563
                },
                 "contour_right8":  {
                    "y":  1901,
                     "x":  1473
                },
                 "right_eyebrow_right_corner":  {
                    "y":  1097,
                     "x":  1643
                },
                 "right_eye_upper_left_quarter":  {
                    "y":  1222,
                     "x":  1540
                },
                 "left_eyebrow_upper_middle":  {
                    "y":  891,
                     "x":  1306
                },
                 "right_eyebrow_upper_right_quarter":  {
                    "y":  1072,
                     "x":  1626
                },
                 "nose_contour_left1":  {
                    "y":  1191,
                     "x":  1380
                },
                 "nose_contour_left2":  {
                    "y":  1388,
                     "x":  1367
                },
                 "mouth_upper_lip_right_contour1":  {
                    "y":  1653,
                     "x":  1498
                },
                 "nose_contour_right1":  {
                    "y":  1225,
                     "x":  1502
                },
                 "nose_contour_right2":  {
                    "y":  1402,
                     "x":  1564
                },
                 "mouth_lower_lip_left_contour2":  {
                    "y":  1743,
                     "x":  1322
                },
                 "contour_right6":  {
                    "y":  1724,
                     "x":  1561
                },
                 "nose_contour_right3":  {
                    "y":  1532,
                     "x":  1521
                },
                 "nose_contour_left3":  {
                    "y":  1522,
                     "x":  1400
                },
                 "left_eye_right_corner":  {
                    "y":  1168,
                     "x":  1345
                },
                 "left_eyebrow_upper_right_quarter":  {
                    "y":  926,
                     "x":  1399
                },
                 "right_eye_upper_right_quarter":  {
                    "y":  1242,
                     "x":  1580
                },
                 "mouth_upper_lip_bottom":  {
                    "y":  1705,
                     "x":  1450
                }
            },
             "attributes":  {
                "emotion":  {
                    "sadness":  0.058,
                     "neutral":  99.511,
                     "disgust":  0.013,
                     "anger":  0.13,
                     "surprise":  0.013,
                     "fear":  0.261,
                     "happiness":  0.013
                },
                 "beauty":  {
                    "female_score":  68.371,
                     "male_score":  68.217
                },
                 "gender":  {
                    "value":  "Male"
                },
                 "age":  {
                    "value":  20
                },
                 "mouthstatus":  {
                    "close":  99.783,
                     "surgical_mask_or_respirator":  0.0,
                     "open":  0.002,
                     "other_occlusion":  0.215
                },
                 "glass":  {
                    "value":  "Normal"
                },
                 "skinstatus":  {
                    "dark_circle":  7.467,
                     "stain":  2.831,
                     "acne":  2.614,
                     "health":  45.221
                },
                 "headpose":  {
                    "yaw_angle":  -41.599888,
                     "pitch_angle":  -4.6719832,
                     "roll_angle":  11.004763
                },
                 "blur":  {
                    "blurness":  {
                        "threshold":  50.0,
                         "value":  0.156
                    },
                     "motionblur":  {
                        "threshold":  50.0,
                         "value":  0.156
                    },
                     "gaussianblur":  {
                        "threshold":  50.0,
                         "value":  0.156
                    }
                },
                 "smile":  {
                    "threshold":  50.0,
                     "value":  8.834
                },
                 "eyestatus":  {
                    "left_eye_status":  {
                        "normal_glass_eye_open":  81.848,
                         "no_glass_eye_close":  0.0,
                         "occlusion":  5.31,
                         "no_glass_eye_open":  0.075,
                         "normal_glass_eye_close":  6.706,
                         "dark_glasses":  6.061
                    },
                     "right_eye_status":  {
                        "normal_glass_eye_open":  0.059,
                         "no_glass_eye_close":  0.0,
                         "occlusion":  46.769,
                         "no_glass_eye_open":  0.006,
                         "normal_glass_eye_close":  0.003,
                         "dark_glasses":  53.163
                    }
                },
                 "facequality":  {
                    "threshold":  70.1,
                     "value":  0.006
                },
                 "ethnicity":  {
                    "value":  "ASIAN"
                },
                 
                "eyegaze":  {
                    
                    "right_eye_gaze":  {
                        
                        "position_x_coordinate":  0.322,
                         
                        "vector_z_component":  0.564,
                         
                        "vector_x_component":  -0.69,
                         
                        "vector_y_component":  -0.453,
                         
                        "position_y_coordinate":  0.199
                    },
                     "left_eye_gaze":  {
                        "position_x_coordinate":  0.606,
                         "vector_z_component":  0.733,
                         "vector_x_component":  0.648,
                         "vector_y_component":  0.206,
                         "position_y_coordinate":  0.481
                    }
                }
            },
             "face_rectangle":  {
                "width":  1152,
                 "top":  852,
                 "left":  521,
                 "height":  1152
            },
             "face_token":  "f5743664f503bf562c97fcf4d62b7ba0"
        }
    ],
     "image_id":  "AlfRCYvws3b3JjuJfNojhQ==",
     "request_id":  "1564128084,35113631-daf7-4bfb-a55a-369272135e57",
     "face_num":  1
}
    """
    leftInfo, rightInfo = getGazeInfo(FaceInfoCorrect)
    result = isTowards(leftInfo, rightInfo)
    print("Result : ", result)
