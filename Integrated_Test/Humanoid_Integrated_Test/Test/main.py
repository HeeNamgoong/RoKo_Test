# -*- coding: utf-8 -*-
# Main code
from Controller import Controller
import cv2
import time

def main():
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #video_filename = "VIDEO/" + time.strftime('%Y-%m-%d_%H-%M-%S') + ".avi"
    #out = cv2.VideoWriter(video_filename, fourcc, 6, (640, 480))
    while not Controller.start():
        continue 

 
if __name__ == "__main__": 
    main() 

