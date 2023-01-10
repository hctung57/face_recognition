# Face Detection Streaming Container for Virtual Classroom
## Future Internet Laboratory(HUST)
### Pull container 
`docker pull hctung57/face-detection:1.0.2`

### Make a rtmp streaming with ffmpeg
**Bước 1:** Cài đặt [ffmpeg](https://linuxize.com/post/how-to-install-ffmpeg-on-ubuntu-18-04/)<br>
**Bước 2:** Cài đặt [rtmp-module nginx](https://docs.peer5.com/guides/setting-up-hls-live-streaming-server-using-nginx/)<br>
**Bước 3:** Tạo luồng streaming `ffmpeg -re -f video4linux2 -i /dev/video0 -r 30 -b:v 512k -f flv rtmp://localhost/live/stream`<br>

### Run Container
1. Run `docker run --name=face-detection -e SOURCE_RTMP_URL="background-blur-service" -e SOURCE_RTMP_PORT=1935 -p 1936:1935 hctung57/face-detection:1.0.2`<br>

**NOTE:**<br>

    SOURCE_RTMP_URL="your source streaming service in kubernetes"
    SOURCE_RTMP_PORT="your source streaming port of the pod {port in service} in kubernetes"

2. See the result `ffplay rtmp://localhost:1936/live/stream`

### NOTE: if you run in local
1. Replace line `export SOURCE_RTMP_URL="$(getent hosts $SOURCE_STREAM_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_RTMP_PORT"` in `nginx.sh` file by `SOURCE_RTMP_URL="your host ip {check by $ip a}:$SOURCE_RTMP_PORT"` <br>
2. Rebuild the container<br>
3. Run `docker run --name=face-detection -e SOURCE_RTMP_PORT=1935 -p 1936:1935 hctung57/face-detection:1.0.2`<br>
