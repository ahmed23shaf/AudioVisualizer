# Graphic Equalizer Display
### About
This equalizer display divides the total frequency spectrum of an incoming audio signal into a discrete set of bars each of which correspond to a frequency component and then provides a real-time visualization of its magnitude. The specific frequencies are listed above each bar (in Hz). The more blue in a bar signifies a higher frequency.

![image](https://github.com/ahmed23shaf/EqualizerDisplay/assets/112600024/d821bcae-d46b-4474-8408-5c981f80cea5)

### Implementation
I used pygame for the overall GUI and NumPy + SciPy for the computations. More specifically, after loading in the audio file data (.wav), I utilized the Fast Fourier Transform (FFT) to discretize a segment of audio into its individual frequency components. The length of the audio segments are inversely determined with `num_bars` which is to say if you increase this variable, the segments would be shorter as you are dividing the spectrum into more bars. Finally, using the results of the windowing effects described above, the code continously updates the current frame allowing us to see the changing magnitudes.
