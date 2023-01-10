from face_lib import face_lib
FL = face_lib()
import cv2
import time
import subprocess
import configargparse

#parser func
def parser_args():
    parser = configargparse.ArgParser(description="Face Recognition NFV FIL HUST",
                            formatter_class=configargparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", "--source_rtmp",
                        help="source stream path")
    return parser.parse_args()

#calculate average fps after exit 
def average_fps(arr):
    sum = 0
    count = 0
    for fps in arr:
        sum += fps
        count += 1
    return sum/count


if __name__ == "__main__":
    #parser init
    args = parser_args()
    source_rtmp = args.source_rtmp

    #URL destination streaming (nginx server)
    rtmp_url = "rtmp://localhost/live/stream"

    #Source Streaming path
    path = f"rtmp://{source_rtmp}/live/stream"
    
    #setup
    font = cv2.FONT_HERSHEY_DUPLEX
    #source video
    cap = cv2.VideoCapture(path)
    WIDTH_INPUT_STREAMING = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    HEIGHT_INPUT_STREAMING = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FPS_INPUT_STREAMING = int(cap.get(cv2.CAP_PROP_FPS))

    REFERENCE_IMAGE = cv2.imread("image.jpg")
    SUM_FRAME_HANDLE = 0
    SUM_FRAME_HAVE_TRUE_OUTPUT = 0

    # Variables to calculate fps
    print_fps_period = 1
    frame_count = 0
    arr = []
    t0 = time.monotonic()
    
    #loop frame by frame
    while(True):
        ret, frame = cap.read()
        if ret == True:
            notify = 'False'
            face_exist, no_faces_detected = FL.recognition_pipeline(frame,REFERENCE_IMAGE)
            if face_exist:
                notify = 'True'
                SUM_FRAME_HAVE_TRUE_OUTPUT += 1
            print("Recognition: {}".format(notify), end="\r")
            # cv2.putText(frame,notify,(25,25), font, 1.0, (255,255,255), 1)
            #fps calculate
            SUM_FRAME_HANDLE += 1
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

recognition_rate = (SUM_FRAME_HAVE_TRUE_OUTPUT/SUM_FRAME_HANDLE)*100
print("AVERAGE FPS: ",average_fps(arr))
print("recognition rate: {:6.2f}".format(recognition_rate),"%")
print("Sum frame : ",SUM_FRAME_HANDLE)

# After the loop release the cap object
cap.release()
