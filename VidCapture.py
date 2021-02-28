import cv2, time, pandas
from datetime import datetime

video = cv2.VideoCapture(0)
firstframe = None
status_list = [None, None]
times = []
dataframe = pandas.DataFrame(columns = ["Start", "End"])

while True:
    check, frame = video.read()
    status = 0

    #ColorCode of Videos:
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (21, 21), 0)

    if firstframe is None:
        firstframe = grey
        continue

    deltaframe = cv2.absdiff(firstframe, grey)
    deltathresh = cv2.threshold(deltaframe, 30, 255, cv2.THRESH_BINARY)[1]
    deltathresh = cv2.dilate(deltathresh, None, iterations = 2)

    #Rectangle around Objects:
    (cnts,_) = cv2.findContours(deltathresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts:
        if cv2.contourArea(cnt) < 10000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    #For Graph:
    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    #Cam Windows:
    cv2.imshow("ContourFrame", frame)
    cv2.imshow("Transparent", deltaframe)
    cv2.imshow("Threshold", deltathresh)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    dataframe = dataframe.append({"Start":times[i], "End":times[i+1]}, ignore_index = True)
dataframe.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows