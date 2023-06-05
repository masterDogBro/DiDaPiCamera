#!/bin/bash


DIR=/home/rtos/proxy
export PYTHONPATH=/home/rtos
export DEVICE=Dida

sudo kill -9 `ps -aux | grep ffmpeg_udp_send | awk '{print $2}'`
sudo kill -9 `ps -aux | grep camera_client | awk '{print $2}'`

cd $DIR
export DEVICE=Dida
export PYTHONPATH=$(dirname ${DIR})

python3 ${DIR}/camera_client.py
sleep 3s
python3 ${DIR}/ffmpeg_udp_send.py