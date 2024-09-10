#!/usr/bin/env python3

import os
import cv2
import numpy as np
import random
import time
import json
from datetime import datetime
from auto_fix_image_levels import adjust_image_colors

# Create a sharpening kernel
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

levels_mode_raw = 0
levels_mode_harsh = 1
levels_mode_friendly = 2
levels_mode_count = 3

sharpen_mode_none = 0
sharpen_mode_harsh = 1
sharpen_mode_friendly = 2
sharpen_mode_count = 3

l_mode = levels_mode_friendly
s_mode = sharpen_mode_friendly


def enhanced_frame(frame):
    if (l_mode == levels_mode_raw):
        l = frame
    else:
        leveled0 = adjust_image_colors(frame)
        if (l_mode == levels_mode_harsh):
            l = leveled0
        else:
            leveled1 = cv2.addWeighted(frame, 0.5, leveled0, 0.5, 0.0)
            l = leveled1

    if (s_mode == sharpen_mode_none):
        s = l
    else:
        sharpened0 = cv2.filter2D(l, -1, kernel)
        if (s_mode == sharpen_mode_harsh):
            s = sharpened0
        else:
            sharpened1 = cv2.addWeighted(l, 0.5, sharpened0, 0.5, 0.0)
            s = sharpened1

    return s


def main():
    global l_mode, s_mode

    # settings
    settings = json.load(open('config.json', 'r'))

    try:
        date_time = datetime.now().strftime(settings['date_time_fmt'])
        mp4_filename = settings['mp4_filename_fmt'] % date_time
    except KeyError as ke:
        raise TypeError(ke.args[0] + ' is a required config setting')

    cap = cv2.VideoCapture(settings["vidcap_camera_index"])
    vidcap_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vidcap_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*(settings['fourcc']))
    print("Video resolution: %dx%d" % (vidcap_w, vidcap_h))
    print("Video FPS: %d" % fps)

    mp4_out = None

    while(1):
        # Take each frame
        _, frame = cap.read()

        res = enhanced_frame(frame)
        cv2.imshow('frame', res)

        if mp4_out is not None:
            # Add this frame to the video
            mp4_out.write(res)

        k = cv2.waitKey(1) & 0xFF
        if k is None:
            continue

        if k == 27:
            break

        if k in [ord('l'), ord('L')]:
            l_mode = (l_mode + 1) % levels_mode_count
            continue

        if k in [ord('s'), ord('S')]:
            s_mode = (s_mode + 1) % sharpen_mode_count
            continue

        if k in [ord('v'), ord('V')]:
            if mp4_out is not None:
                # Close the video output
                print("Releasing MP4 Video Writer")
                mp4_out.release()
                mp4_out = None
            else:
                date_time = datetime.now().strftime(settings['date_time_fmt'])
                mp4_filename = os.path.expanduser(settings['mp4_filename_fmt']) % date_time

                # Open the video output
                print("Capturing MP4 Video to " + mp4_filename)
                mp4_out = cv2.VideoWriter(mp4_filename, fourcc, fps, (vidcap_w, vidcap_h))
            continue

        if k in [ord('p'), ord('P')]:
            date_time = datetime.now().strftime(settings['date_time_fmt'])
            png_filename = os.path.expanduser(settings['png_filename_fmt']) % date_time

            # Save an image
            print("Capturing PNG still image to " + png_filename)
            cv2.imwrite(png_filename, res)

    cv2.destroyAllWindows()

    if mp4_out is not None:
        # Close the video output
        print("Releasing MP4 Video Writer")
        mp4_out.release()


if __name__ == '__main__':
    main()
