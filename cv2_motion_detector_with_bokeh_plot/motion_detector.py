import cv2, time, pandas, matplotlib, seaborn as sns
from datetime import datetime

first_frame = None
status_list = [None, None]
times=[]
time1 = []
df = pandas.DataFrame(columns = ["Start","End"])

video = cv2.VideoCapture(0)


while True:
	#for each frame, track the status(0 - no object>10k px, 1 - object present)
	status = 0
	check, frame = video.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray,(21, 21), 0)	

		
	#do this on first iteration to have a first reference frame
	if first_frame is None:
		first_frame = gray
		continue


	#define the image difference between original static image, and following frames	
	delta_frame = cv2.absdiff(first_frame, gray)
	#set threshold diff btween delta, static;classify each difference pixel as below thresh(black) or above(white)
	thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
	#smooth out the resultant threshold difference frame
	thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
	#find contours of all objects detected by threshold difference frame
	(_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	#ignore contours smaller than 10000 pixels, draw rectangles around countours greater than that
	for contour in cnts:
		if cv2.contourArea(contour) < 8000:
			continue
		status = 1
		#create a rectangle bound around countour and take its params to pass to the rectangle method
		(x,y,w,h) = cv2.boundingRect(contour)
		cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 3)
		
	#track status of each frame and record it in status_list		
	status_list.append(status)
	status_list = status_list[-2:]	

	#check if status has changed from 0 to 1, and record the time of that event in 'times' list
	if status_list[-1] == 1 and status_list[-2] == 0:
		times.append(datetime.now())
	#check if status has changed from 1 to 0, and record the time of that event in 'times' list
	if status_list[-1] == 0 and status_list[-2] == 1:
		times.append(datetime.now())
	time1.append(datetime.now())
	cv2.imshow("Capturing", gray)
	cv2.imshow("delta",delta_frame)
	cv2.imshow("thresh", thresh_frame)	
	cv2.imshow("rectangleframe", frame)


	key = cv2.waitKey(1)	
	
	
	if key == ord('q'):
		if status == 1:
			times.append(datetime.now())
		break
	
for i in range(0,len(times),2):
	df = df.append({"Start":times[i],"End":times[i+1]}, ignore_index = True)

#Save times of motion start and end in Times.csv
df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()

