#!/bin/bash
echo "nginx: starting up nginx..."
/usr/local/nginx/sbin/nginx
echo "nginx is running..."
export SOURCE_RTMP_URL="$(getent hosts $SOURCE_STREAM_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_RTMP_PORT"
echo "exported url of source streaming: $SOURCE_RTMP_URL"
echo "starting face detection func..."

python3 face_detection.py -s $SOURCE_RTMP_URL

while true
do :
exit_status=$?
if [ "${exit_status}" -eq 0 ];
then
    echo "Regenerate service ip address..."
    export SOURCE_RTMP_URL="$(getent hosts $SOURCE_STREAM_SERVICE | awk '{ print $1 ;exit }'):$SOURCE_RTMP_PORT"
    echo "exported url of source streaming: $SOURCE_RTMP_URL"
    echo "Restarting face detection func..."
    python3 face_detection.py -s $SOURCE_RTMP_URL
fi
sleep 1
done

# Just a loop to keep the container running
while true; do :; done