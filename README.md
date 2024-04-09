# Silent Rave Server

This repo contains the necessary tooling for organizing a silent rave, bring-your-own-device style, everyone with their own headphones.
- FastAPI + Uvicorn server streaming live music through HLS protocol.
- NGINX reverse proxy to better serve index.html and HLS files/playlist
- Mac Client for forwarding all live audio from BlackHole to the server. Audio is uploaded through HTTP.

Last time, I hosted everything on a Google Cloud Compute Engine instance with something like 4GB ram and 4 CPUs.
Note, for some reason audio is broken when directly attempting to read the loopback device from ffmpeg. Instead, reading the audio from SOX and piping to ffmpeg through stdout works!

## Launch the server

Start the server (from cloud instance)
```
./run-server.sh
```

Start the streaming client (on your mac)
```
./stream-from-mac.sh
```

Check out the web page where appropriate. You should see something like this.

![image](https://github.com/gabrielhuang/silent-rave-server/assets/7798468/959a1c7e-cc32-4efa-9f4b-5693d2672bf8)

## Setup "Guide"

The following are more notes than an actual guide to set everything up.

- Install BlackHole driver
- Create a multi output device
- Install Pyaudio.
- Install sox


```bash
brew install portaudio
pip3 install pyaudio pydub
brew install ffmpeg
```

My server
https://console.cloud.google.com/compute/instances?onCreate=true&project=naivepsychology-22c0e 


Debug: stream to file
```
ffmpeg -f avfoundation -i ":0" -c:a aac -b:a 128k -vn -hls_time 2 -hls_list_size 5 -hls_flags delete_segments -f hls output.m3u8
```

SSH to gogole cloud
```
gcloud compute ssh --zone "northamerica-northeast1-a" "silent-rave" --project "naivepsychology-22c0e"
```

Make sure to configure HTTP ports correctly! (VPC network section)

Find the device name on mac (Blackhole 2ch?)
```
ffmpeg -list_devices true -f avfoundation -i dummy
sox -V6 -n -t coreaudio junkname  # "BlackHole 2ch"
```

Start nginx
```
sudo systemctl reload nginx
sudo systemctl start nginx
```


## Limitations
- Audio sync seems to be +/- 10 sec which is not great but usable.
- I haven't figured out HTTPS stuff, so everything is pretty insecure now. lol
