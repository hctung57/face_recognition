
## Yêu cầu hệ điều hành Ubuntu và ngôn ngữ lập trình Python<br>
## Video tĩnh
**Bước 1:** Cài đặt [face_lib](https://github.com/a-akram-98/face_lib?ref=pythonawesome.com)<br>
**Bước 2:** Thay đổi đường dẫn tới video và ảnh xác minh rồi chạy file. <br>
## Hướng dẫn chạy (streaming)
**Bước 1:** Cài đặt **v4l2loopback** (hướng dẫn cài đặt và sử dụng [v4l2loopback](https://github.com/umlaeute/v4l2loopback))<br>

**Bước 2:** Cài đặt [face_lib](https://github.com/a-akram-98/face_lib?ref=pythonawesome.com) và các thư viện liên quan khác trong phần khai báo thư viện trong  recognition.py.<br>

**Bước 3:** Tạo các host camera ảo trên thiết bị bằng câu lệnh<br>

```sudo modprobe v4l2loopback video_nr=2,3,4,5 card_label="backgroud-blur","face-detect","recogition","backup"```

*Mặc định trên ubuntu sẽ có 1 host là /dev/video0 là kênh để webcam trả dữ liệu cho máy. Câu lệnh này sẽ tạo ra các host camera ảo bằng v4l2loopback (/dev/video2, /dev/video3, ...).*<br>

**Bước 4:** Tạo luồng stream qua các NFV.<br>
*Chú ý:*
* Thay đổi nguồn của video đến tại: ```vid = cv2.VideoCapture(source_video)```
* Thay đổi đích của luồng stream tại: ```cam = pyfakewebcam.FakeWebcam('host_camera',int(width), int(height))``` với host_camera='/dev/video*'
 
 **Bước 5:** Cuối cùng thử tạo một luồng stream tới 1 máy khác bằng ffmpeg với đầu vào là host của function cuối cùng trong chuỗi.
 
 
