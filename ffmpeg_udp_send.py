# coding: utf-8

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput
import time


class Config:
    camera_client_addr = ('192.168.137.1', 60001)


class PiCamera:

    def __init__(self):
        self.picam2 = Picamera2()
        self.video_config = self.picam2.create_video_configuration()
        self.picam2.configure(self.video_config)

        # iperiod=15 i帧频率，每15个插一个i帧
        # repeat=True 在每帧内(I帧)重复流的序列头，即使流被中途接收，也能有效解析帧头
        self.encoder = H264Encoder(repeat=True, iperiod=15)
        # self.encoder = H264Encoder()

        # 使用udp传输，目标是宿主机12345端口 -f mpegts udp://192.168.137.1:12345
        # 增加0延迟参数 -tune zerolatency
        # preset ultrafast（转码速度最快，视频往往也最模糊）-preset ultrafast
        self.output = FfmpegOutput(
            "-tune zerolatency -preset ultrafast -f mpegts udp://{0}:{1}".
            format(Config.camera_client_addr[0],
                   Config.camera_client_addr[1]))

        # output = FfmpegOutput("-f mpegts udp://192.168.137.1:12345")
        # output = FfmpegOutput("-tune zerolatency -f mpegts udp://127.0.0.1:12345")
        # output = FfmpegOutput("-tune zerolatency -f rtsp rtsp://192.168.137.1:12345/live.sdp")

        self.encoder.output = self.output

    def start(self):
        self.picam2.start_encoder(self.encoder)
        self.picam2.start()
        # 需要持久的视频流
        # while True:
        #    time.sleep(1)

        # The file is closed, but carry on streaming to the network.
        time.sleep(9999999)


# output2 = FileOutput()
# output2 = FileOutput()
# encoder.output = [output1, output2]
# encoder.output = [output1, output2]
# encoder.output = [output1, output2]
# encoder.output = output

# Start streaming to the network.
# picam2.start_encoder(encoder)
# picam2.start()
# time.sleep(5)

# Start recording to a file.
# output2.fileoutput = "test.h264"
# output2.start()
# time.sleep(5)
# output2.stop()

def main():
    camera = PiCamera()
    camera.start()


if __name__ == "__main__":
    main()
