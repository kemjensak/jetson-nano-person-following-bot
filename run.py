import jetson.inference
import jetson.utils
import RPi.GPIO as GPIO
import time
#핀 세팅
L_pin = 33    
R_pin = 32

#핀 모드, PWM 세팅
GPIO.setmode(GPIO.BOARD)
    
GPIO.setup(L_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(R_pin, GPIO.OUT, initial=GPIO.LOW)

L = GPIO.PWM(L_pin, 100)
R = GPIO.PWM(R_pin, 100)

#0%로 PWM 시작
L.start(0)
R.start(0)


#물체인식 Model, Threshold(해당 %이상만 결과로 return)세팅
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

#사용할 카메라와 해상도 지정 
camera = jetson.utils.gstCamera(1280, 720, "/dev/video0")

display = jetson.utils.glDisplay()

#모터제어 함수, 중앙에서 멀어질수록 더 빠른 각속도로 돌도록 함(바퀴속도 차이를 크게 함)
#추후 적절한 수식으로 
def motor(target):
    if target < 620:
        L.ChangeDutyCycle(50)
        R.ChangeDutyCycle(60)
        
        if target < 400:
            L.ChangeDutyCycle(50)
            R.ChangeDutyCycle(70)
            
            if target < 200:
                L.ChangeDutyCycle(50)
                R.ChangeDutyCycle(80)

    elif target > 660:
        L.ChangeDutyCycle(60)
        R.ChangeDutyCycle(50)
        
        if target > 880:
            L.ChangeDutyCycle(70)
            R.ChangeDutyCycle(50)

            if target > 1080:
                L.ChangeDutyCycle(80)
                R.ChangeDutyCycle(50)
    else:
        L.ChangeDutyCycle(55)
        R.ChangeDutyCycle(55)
        
#메인 반복함수 시작
try:
    while True:
        img, width, height = camera.CaptureRGBA()  #물체인식 사전 세팅
        detections = net.Detect(img, width, height) #인식후 결과 저장
        display.RenderOnce(img, width, height) #인식결과 창으로 보여줌
        display.SetTitle("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS())) #창 Title 세팅

        
        #사람에 대한 인식 결과만 이용
        for i in detections:
            
            if i.ClassID == 1: # Class ID 1이 person

                motor(i.Center[0])
#motor 함수에 bounding box의 Center 좌표 전달
            else:
                print("no person")
                
finally:
    L.stop()
    R.stop()
    GPIO.cleanup()
# exception 발생 시 PWM 정지 및 GPIO 설정 초기화
