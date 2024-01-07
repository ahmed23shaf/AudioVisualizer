import wave
import numpy
import pygame
from pygame.locals import *
from scipy.fft import fft, fftfreq

class Visualizer:
    def __init__(self, audio_fp, bars, bar_y, bar_x, fps_, screen_, freq_text):
        """
        Initializes an audio visualization.

        @param audio_fp (str): File path of the audio file
        @param bars (int): Number of bars in the visualizer
        @param bar_y (int): Height of a bar
        @param bar_x (int): Width of a bar
        @param fps_ (int): Frames per second
        @param screen_ (pygame.Surface): Pygame screen object
        @param freq_text (pygame.font.Font): Font for frquencies
        """
        self.audio_file_path = audio_fp
        self.num_bars = bars
        self.bar_height = bar_y
        self.bar_width = bar_x
        self.fps = fps_
        self.screen = screen_
        self.freq_font = freq_text

        # Load audio file and extract parameters
        self.audio_file = wave.open(audio_fp, 'rb')
        self.audio_params = self.audio_file.getparams()
        self.num_channels, self.sample_width, self.sample_rate, self.num_frames = self.audio_params[:4]
        self.audio_data_str = self.audio_file.readframes(self.num_frames)
        self.audio_file.close()
        self.audio_data = numpy.fromstring(self.audio_data_str, dtype=numpy.short)
        self.audio_data.shape = -1, 2
        self.audio_data = self.audio_data.T

        self.current_frame = self.num_frames

    def visualizer(self, frame_number):
        """
        Updates the visualizer based on the current frame.

        @param frame_number (float): Current frame number.
        """
        self.current_frame = int(frame_number)
        amplitudes, frequencies = self.get_amplitudes_and_frequencies()
        amplitudes = [min(self.bar_height, int(i ** (1 / 2.5) * self.bar_height / 100)) for i in amplitudes]
        self.draw_bars(amplitudes, frequencies)

    def update(self):
        """
        Updates the visualizer status based on the current frame.

        @return (str): Status of the visualizer ("stopped" if the end is reached, otherwise None).
        """
        self.current_frame -= self.sample_rate / self.fps
        if self.current_frame > 0:
            self.visualizer(self.current_frame)
        else:
            return "stopped"

    def get_current_time(self):
        """
        Returns the current playback time in HH:MM:SS format.

        @return (str): Current playback time.
        """
        seconds = max(0, pygame.mixer.music.get_pos() / 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def get_amplitudes_and_frequencies(self):
        """
        Computes and returns amplitudes and frequencies using Fast Fourier Transform (FFT).

        @return (tuple): A tuple containing amplitudes and frequencies.
        """
        # Extract windowed block for current frame
        start_frame = self.num_frames - self.current_frame
        end_frame = start_frame + self.num_bars
        audio_segment = self.audio_data[0][start_frame:end_frame]

        amplitudes = abs(fft(audio_segment))
        frequencies = fftfreq(len(amplitudes), 1 / self.sample_rate)

        return amplitudes, frequencies

    def draw_bars(self, amplitudes, frequencies):
        """
        Draws bars on the screen based on amplitudes and frequencies.
        A higher frequency results in a more blueish appeareance for a frequency component bar.

        @param amplitudes (list): List of amplitudes.
        @param frequencies (list): List of frequencies.
        """
        bars = []
        drawn_frequencies = set()

        for i, height in enumerate(amplitudes):
            frequency = abs(frequencies[i])

            if frequency not in drawn_frequencies:
                color = (255 - int(frequency * 255 / max(frequencies)) + 50, 0, int(frequency * 255 / max(frequencies)))
                color = tuple(max(0, min(255, c)) for c in color)
                bars.append([len(bars) * self.bar_width, 50 + self.bar_height - height, self.bar_width - 1, height, frequency, color])
                drawn_frequencies.add(frequency)

        for bar in bars:
            pygame.draw.rect(self.screen, bar[5], bar[:4], 0)

        for bar in bars:
            frequency_text = self.freq_font.render(f'{bar[4]:.0f}', True, (255, 255, 255))
            text_rect = frequency_text.get_rect(center=(bar[0] + self.bar_width // 2, 50 + self.bar_height - bar[3] - 15))
            self.screen.blit(frequency_text, text_rect.topleft)
