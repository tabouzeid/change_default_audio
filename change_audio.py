import os
import argparse
from FFProbeInfo import FFProbeInfo


def main(args):
    info = FFProbeInfo(args['i'], args['fp'])
    info = info.probe()
    if info is None:
        print("Path no found")
        exit(1)
    elif len(info.audio) == 1:
        print 'There is only 1 audio stream, there is nothing to switch.'
        exit(1)
    else:
        current_default_audio_index = get_current_default(info)
        desired_default_audio_index = get_desired_default(info, current_default_audio_index)
        print 'Switching default audio from %d to %d' % (current_default_audio_index, desired_default_audio_index)
        command = '%s -i \"%s\" -map 0 -c:s copy -disposition:a:%d default -disposition:a:%s none \"%s\"' % (args['fm'], info.path, desired_default_audio_index, current_default_audio_index, args['o'])
        print command
        exit_status = os.system(command)
        exit_status = os.WEXITSTATUS(exit_status)
        if exit_status == 0:
            print 'it worked!'
        else:
            print 'it failed!'


def get_current_default(ffprobe_info):
    if ffprobe_info is not None:
        default_audio_index = ffprobe_info.get_default_audio()
        if default_audio_index >= 0:
            for index, lang in enumerate(ffprobe_info.audio_names):
                if index == default_audio_index:
                    print '%d: %s (default)' % (index + 1, lang)
                else:
                    print '%d: %s' % (index + 1, lang)
        elif default_audio_index == -1 and len(ffprobe_info.audio) > 1:
                print 'No default audio specified and more than one audio stream exists'
        return default_audio_index
    return None


def get_desired_default(info, current_default_audio_index):
    desired_default_audio_index = input('Please select desired default audio: ')
    desired_default_audio_index = int(desired_default_audio_index) - 1
    if desired_default_audio_index >= len(info.audio) or desired_default_audio_index < 0:
        print 'Invalid Selection'
        exit(1)
    if desired_default_audio_index == current_default_audio_index:
        print 'Current and desired default audio stream are  the same'
        exit(1)
    return desired_default_audio_index


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', help='Path to the input video file', metavar='/path/to/input/video.mp4', type=str, required=True)
    parser.add_argument('-o', help='Path to the output video file', metavar='/path/to/output/video.mp4', type=str, required=True)
    parser.add_argument('--fm', help='Path to the ffmpeg command', metavar='/path/to/ffmpeg', type=str, required=False, default='ffmpeg')
    parser.add_argument('--fp', help='Path to the ffprobe command', metavar='/path/to/ffprobe', type=str, required=False, default='ffprobe')
    args = parser.parse_args()
    print vars(args)
    main(vars(args))

