# coding: utf-8

import nvwave
import queue
import struct
import threading
from contextlib import AbstractContextManager
from crystal_tts import Mimic3Settings, Mimic3TextToSpeechSystem, SSMLSpeaker, AudioResult
from dataclasses import dataclass


# Sentinel
_missing = object()
_stop_playing = object()


@dataclass
class CrystalSpeechPlayer(AbstractContextManager):
    tts_settings: Mimic3Settings

    def __post_init__(self):
        self.tts = Mimic3TextToSpeechSystem(self.tts_settings)
        self.ssml_speaker = SSMLSpeaker(self.tts)
        self._players = {}
        self.audio_result_queue = queue.Queue(32)
        self.playing_thread = threading.Thread(target=self.player_func)
        self.playing_thread.daemon = True
        self.playing_thread.start()

    def close(self):
        self.audio_result_queue.put_nowait(_stop_playing)
        self.tts.shutdown()
        for player in self._players.values():
            player.close()
        self._players.clear()

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _get_or_create_player(self, sampling_rate, bits_per_sample, channels, output_device=_missing):
        key = (sampling_rate, bits_per_sample, channels)
        if key not in self._players:
            kwargs = {
                "channels": channels,
                "samplesPerSec": sampling_rate,
                "bitsPerSample": bits_per_sample,
                "buffered": True
            }
            if output_device is not _missing:
                kwargs["outputDevice"] = output_device
            self._players[key] = nvwave.WavePlayer(**kwargs)
        return self._players[key] 

    def speak_ssml(self, ssml):
        for res in self.ssml_speaker.speak(ssml):
            if not isinstance(res, AudioResult):
                continue
            self.audio_result_queue.put_nowait(res)

    def player_func(self):
        while True:
            try:
                res = self.audio_result_queue.get()
            except queue.Empty:
                continue
            else:
                if res is _stop_playing:
                    return
                player = self._get_or_create_player(
                    sampling_rate=res.sample_rate_hz,
                    bits_per_sample=res.sample_width_bytes*8,
                    channels=res.num_channels
                )
                player.feed(res.audio_bytes)