import json
import os
from subprocess import Popen, PIPE
import logging
import locale

logger = logging.getLogger(__name__)

console_encoding = locale.getdefaultlocale()[1] or 'UTF-8'

class FFProbeInfo(object):
    """
    Information about media object, as parsed by ffprobe.
    The attributes are:
      * format - a MediaFormatInfo object
      * streams - a list of MediaStreamInfo objects
      * path - path to file
    """
    def __init__(self, video_path, ffp_path):
        """
        :param posters_as_video: Take poster images (mainly for audio files) as
            A video stream, defaults to True
        """
        self.rawJson = {}
        self.formatInfo = FFProbeFormatInfo({})
        self.streamInfo = FFProbeStreamInfo({})
        self.path = video_path
        self.ffprobe_path = ffp_path

    def __repr__(self):
        return 'MediaInfo(audio_languages=%s)' % self.audio_names

    @property
    def video(self):
        return self.streamInfo.videos

    @property
    def posters(self):
        return [s for s in self.streams if s.attached_pic]

    @property
    def audio(self):
        return self.streamInfo.audios

    @property
    def audio_names(self):
        result = []
        for s in self.audio:
            if s["tags"] is not None:
                result.append(s["tags"]["language"].encode('utf-8'))
        return result

    def get_default_audio(self):
        for idx, a in enumerate(self.audio):
            if a.has_key("disposition") and a["disposition"].has_key("default") and a["disposition"]["default"] == 1:
                return idx
        return -1

    @property
    def subtitle(self):
        return self.streamInfo.subtitles

    @property
    def attachment(self):
        result = []
        for s in self.rawJson["streams"]:
            if s["codec_type"] == 'attachment':
                result.append(s)
        return result

    def probe(self):
        if not os.path.exists(self.path):
            return None

        stdout_data = self._get_stdout([self.ffprobe_path, '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', self.path])
        parsed_data = json.loads(stdout_data)
        if not parsed_data["format"] and len(parsed_data["streams"]) == 0:
            return None

        self.rawJson = parsed_data
        self.streamInfo = FFProbeStreamInfo(self.rawJson["streams"])
        self.formatInfo = FFProbeFormatInfo(self.rawJson["format"])

        return self

    @staticmethod
    def _spawn(cmds):
        clean_cmds = []
        try:
            for cmd in cmds:
                clean_cmds.append(str(cmd))
            cmds = clean_cmds
        except:
            logger.exception("There was an error making all command line parameters a string")
        logger.debug('Spawning ffmpeg with command: ' + ' '.join(cmds))
        return Popen(cmds, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                     close_fds=(os.name != 'nt'), startupinfo=None)

    def _get_stdout(self, cmds):
        p = self._spawn(cmds)
        stdout_data, stderr = p.communicate()
        logger.debug('stderr:\n', stderr)
        return stdout_data.decode(console_encoding, errors='ignore').encode('utf-8')


class FFProbeFormatInfo(object):
    """
    Information about media object, as parsed by ffprobe.
    The attributes are:
      * format - a MediaFormatInfo object
      * streams - a list of MediaStreamInfo objects
      * path - path to file
    """

    def __init__(self, format_info):
        """
        :param posters_as_video: Take poster images (mainly for audio files) as
            A video stream, defaults to True
        """
        self.rawJson = format_info

class FFProbeStreamInfo(object):
    def __init__(self, streamInfo):
        """
        :param posters_as_video: Take poster images (mainly for audio files) as
            A video stream, defaults to True
        """
        self.rawJson = streamInfo
        self.streamsByType = {}
        for stream in self.rawJson:
            codec_type = "Unknown Stream Type"
            streams_for_type = []
            if stream.has_key("codec_type"):
                codec_type = stream["codec_type"]
            if self.streamsByType.has_key(codec_type):
                streams_for_type = self.streamsByType[codec_type]
            else:
                self.streamsByType[codec_type] = streams_for_type
            streams_for_type.append(stream)

    @property
    def videos(self):
        """
        All video streams, or None if there are no video streams.
        """
        if self.streamsByType.has_key("video") is not None:
            return list(self.streamsByType["video"])
        return []

    @property
    def audios(self):
        if self.streamsByType.has_key("audio"):
            return list(self.streamsByType["audio"])
        return []

    @property
    def subtitles(self):
        if self.streamsByType.has_key("subtitle") is not None:
            return list(self.streamsByType["subtitle"])
        return []
