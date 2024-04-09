#!/bin/bash
ffmpeg  -f pulse -i auto_null.monitor -c:a aac -b:a 128k -ar 44100 -vn -hls_time 6 -hls_list_size 5 -hls_flags delete_segments -f hls -hls_segment_filename '/home/ffmpeguser/silent-rave-server/static/hls/file_%09d.ts' '/home/ffmpeguser/silent-rave-server/static/hls/output.m3u8'
