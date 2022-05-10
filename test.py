from face_lib import face_lib
FL = face_lib()
import cv2
import time
# import pyfakewebcam

def average_fps(arr):
    sum = 0
    count = 0
    for fps in arr:
        sum += fps
        count += 1
    return sum/count
#setup
font = cv2.FONT_HERSHEY_DUPLEX
#source video
vid = cv2.VideoCapture(0)
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT) 
img_to_verify = cv2.imread("../Pictures/1.jpg")
sum_frame = 0
sum_face_true = 0
print_fps_period = 1
frame_count = 0
arr = []
t0 = time.monotonic()
#setup host camera (for streaming)
# print("Live camera in /dev/video4")
# cam = pyfakewebcam.FakeWebcam('/dev/video4',int(width), int(height))

while(True):
    ret, frame = vid.read()
    if ret == True:
        notify = 'False'
        face_exist, no_faces_detected = FL.recognition_pipeline(frame,img_to_verify)
        if face_exist:
            notify = 'True'
            sum_face_true += 1
        cv2.putText(frame,notify,(25,25), font, 1.0, (255,255,255), 1)
        #schedule frame to host camera (for streaming)
        # cam.schedule_frame(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        #cv2 show
        cv2.imshow("frame",frame)
        #fps calculate
        sum_frame += 1
        frame_count += 1
        td = time.monotonic() - t0
        if td > print_fps_period:
            current_fps = frame_count / td
            arr += [current_fps]
            print("FPS: {:6.2f}".format(current_fps), end="\r")
            frame_count = 0
            t0 = time.monotonic()
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #break th loop
    else:
        break

recognition_rate = (sum_face_true/sum_frame)*100
print("FPS: ",average_fps(arr))
print("recognition rate: {:6.2f}".format(recognition_rate),"%")
print("Sum frame : ",sum_frame)
print("CPU: ",sum_cpu/sum_frame)

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
# cam.print_capabilities()