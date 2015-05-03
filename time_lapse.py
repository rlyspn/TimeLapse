#!/usr/bin/env python

import json
import picamera
import re
import os
import subprocess as sp
import sys
import time

'''
Author: Riley Spahn
Date: 5/2/2014

Script for creating time lapse videos on a RaspberryPi.
'''


def read_config(config_file=None):
    """
    Returns the configurations from the config file or the default values for
    each field.
    """
    default_width = 800
    default_height = 600
    default_quality = 25
    default_image_dir = 'images'
    default_video_file = 'time_lapse.mp4'
    default_frames_per_second = 16

    if config_file is None:
        return {'width': default_width, 'height': default_height,
                'quality': default_quality, 'image_dir': default_image_dir,
                'video_file': default_video_file,
                'frames_per_second': default_frames_per_second}
    with open(config_file, 'r') as fd:
        return_config = {}
        json_str = fd.read()
        json_data = json.load(json_str)
        return_config['width'] = json_data.get('width', default_width)
        return_config['height'] = json_data.get('height', default_height)
        return_config['quality'] = json_data.get('quality', default_quality)
        return_config['image_dir'] = json_data.get('image_dir',
                                                   default_image_dir)
        return_config['video_file'] = json_data.get('video_file',
                                                    default_video_file)
        return_config['frames_per_second'] = json_data.get('frames_per_second',
                                                    default_frames_per_second)
        return return_config


def capture_image(width=800, height=600, quality=25, image_dir='images'):
    """
    Captures an image of size <width> and <height> at <quality> and stores it
    in the directory <image_dir>.
    """
    file_count = len(os.listdir(image_dir))
    img_file = 'image_%05d.jpg' % file_count
    img_path = os.path.join(image_dir, img_file)
    with picamera.PiCamera() as camera:
        camera.resolution = (width, height)
        time.sleep(2)
        camera.capture(img_path, quality=quality)
        print 'Capturing: %s' % img_path


def encode_video(frames_per_second, image_dir, video_file):
    """
    Usese libav to encode the images in <image_dir> into the video file
    <video_file>.
    """
    print 'Rendering time lapse.'
    image_partial_path = os.path.join(image_dir, 'image_')
    av_cmd = 'avconv -r %d -qscale 2 -i %s%%05d.jpg %s' % (frames_per_second,
                                                           image_partial_path,
                                                           video_file)
    if os.path.isfile(video_file):
        os.remove(video_file)
    os.system(av_cmd)


def get_disk_usage():
    """
    Returns the approximate disk space used on the root file system.
    """
    df_proc = sp.Popen('df', stdout=sp.PIPE)
    df_out = df_proc.stdout.read()
    return int(re.search(r'(\d+)%', filter(lambda x: 'rootfs' in x,
               df_out.split('\n'))[0]).group(1))


def handle_disk_usage(image_dir):
    disk_usage = get_disk_usage()
    if disk_usage > 90:
        os.system('rm -rf %s/*' % image_dir)


def time_lapse_loop(tl_config):
    images_per_render = 10
    time_between_images = 60
    index = 0
    while True:
        capture_image(tl_config['width'], tl_config['height'],
                      tl_config['quality'], tl_config['image_dir'])
        index += 1
        time.sleep(time_between_images)
        if index % images_per_render == 0:
            encode_video(tl_config['frames_per_second'],
                         tl_config['image_dir'],
                         tl_config['video_file'])

tl_config = read_config(sys.argv[1]) if len(sys.argv) == 2 else read_config()
time_lapse_loop(tl_config)
