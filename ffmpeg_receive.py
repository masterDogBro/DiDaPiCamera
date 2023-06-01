# coding: utf-8

import os

commandArgs = [
    #
    "-probesize", "32",
    #
    "-sync", "ext",
    #
    "-i", "udp://127.0.0.1:12345?listen",
]
# os.system("ffplay.exe " + "".join(commandArgs))
print("ffplay.exe " + " ".join(commandArgs))
