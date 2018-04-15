import argparse
import datetime
import imutils
import RPi.GPIO as GPIO
import time
import cv2

# GPIO setup çıkışları bağlanıyor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setwarnings(False)
# argüman ayrıştırıcısını oluşturma
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# video için argüman yoksa kameradan oku
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)
# varsa,argümandan oku
else:
	camera = cv2.VideoCapture(args["video"])

#videodaki ilk frame başlatılıyor

firstFrame = None
a=50
while True:
	# mevcut frame yakalanır ve ortam durumu söylenir
	(grabbed, frame) = camera.read()
	text = "Ortam Temiz"
	GPIO.output(11,GPIO.LOW)
	GPIO.output(18,GPIO.LOW)
	if not grabbed:
		break

	# frame penceresinin boyutları ayarlanır, görüntü grileştirilir, ve blur filtresi uygulanır
	frame = imutils.resize(frame, width=320)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	if firstFrame is None:
		firstFrame = gray
		continue

	# ilk frame ile mevcut frame arasındaki fark hesaplanıyor
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# görüntü genişletilir ve dış hatlar bulunur
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	for c in cnts:
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# contour hesaplanır ve frame'e yazılır.ardından yazı güncellenmeli
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Ortamda Birisi Var"
		GPIO.output(11,GPIO.HIGH)
		GPIO.output(18,GPIO.HIGH)
		a+=5
		if a % 40 == 0:
                    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                    goruntu_adi = "opencv_goruntuler_{}.jpg".format(a)
                    cv2.imwrite(goruntu_adi, frame)
                    continue
	# frame penceresinde durum adı belirtilir
	cv2.putText(frame, "Oda Durumu {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# kullanıcı bir tuşa basana kadar kayda devam et ve pencere açık kalsın
	cv2.imshow("Güvenlik Kamerası", frame)
	key = cv2.waitKey(1) & 0xFF

	# tuş olarak q atandı.q ya basıldığı anda döngüden çıkacak
	if key == ord("q"):
		break


GPIO.cleanup()
camera.release()
cv2.destroyAllWindows()



