# Change Default Audio
I've got a few videos that have more than one audio stream on them. I got annoyed that the default audio stream was not the one I wanted so I decided to write this to resolve that issue.

## How it works
The contents of a video file can be described in a list of streams. There are video, audio and subtitle streams. In our case we are interested in the disposition section of the audio stream informaiton because it has a default flag which indicates which audio stream (assuming there's more than one) is the one to use be default. This script changes that flag from the current audio stream to the one that you choose.

**Warning!** The process creates a new file instead of modifying the old one. It also converts the encoding of the content. The specifics of the conversion can be seen in the output (example below):
```
Stream mapping:
  Stream #0:0 -> #0:0 (mpeg4 (native) -> h264 (libx264))
  Stream #0:1 -> #0:1 (aac (native) -> vorbis (libvorbis))
  Stream #0:2 -> #0:2 (aac (native) -> vorbis (libvorbis))
  Stream #0:3 -> #0:3 (copy)
  Stream #0:4 -> #0:4 (copy)
  Stream #0:5 -> #0:5 (copy)
```

## Dependencies
[python](https://www.python.org/)

[ffmpeg](https://www.ffmpeg.org/)

ffprobe - Should already come with ffmpeg

## How to run the script
This. assumes that when you type ```ffmpeg```. or ```ffprobe``` in the terminal it will work.
```
python -i "/path/to/the/file" -o "/path/to/output/file"
```
If the path to ```ffmpeg``` or ```ffprobe``` is different then provide the proper path in the script arguments
```
python -i "/path/to/the/file" -o "/path/to/output/file" --ffm "/usr/local/bin/ffmpeg" --ffp "/usr/local/bin/ffprobe"
```
