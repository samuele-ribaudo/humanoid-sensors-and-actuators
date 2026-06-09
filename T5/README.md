# Humanoid Sensors and Actuators
## Group 5
| Name | Matr. # | Email |
|------|---------|-------|
| Samuele Ribaudo | 03821248 | samuele.ribaudo@tum.de |
| Hong Yan Jun  | 03813507 | go75kes@mytum.de |
| Alessandro Canalicchio | 03796273 | go73xix@mytum.de |
| Niklas Peter | 03812287 | n.peter@tum.de |
| Emile Gebrael | 03812968 | emile.gebrael@tum.de |

We recomend viewing this report [here con GitHub ↗](https://github.com/samuele-ribaudo/humanoid-sensors-and-actuators/tree/main/T5), or with a markdown viewer.

# Tutorial 5

Course Instructor: Dr.-Ing. J. Rogelio Guadarrama Olvera
hsa-lecture.ics@xcit.tum.de

Summer Semester 2026

## Acoustic Sensors and Signal Processing (57 points)

In this tutorial we will refresh some basics of signal processing including correlation, Fast Fourier Transform (FFT) and filtering. All tasks are solvable with Python, Matlab, Octave or Scilab with a slightly varying syntax.

**Note:** You may use any of the above programming languages. However, we strongly recommend using Jupyter Notebooks (python) to solve and visualize all the tutorial. We will only support installation/setup questions related to python.

## 1 Sound Source Localization (8 points)

### Report

**R.1.1 (3 points)** Find the expression to determine the azimuth angle of a sound source for a system with two microphones. Derive the equations shown in the slides of Lecture 3 step by step.

1. Calculate the path length difference using the speed of sound $c$ and the time delay $\Delta t$:
$$\text{Distance}=c\Delta t$$

2. Determine the geometric extra distance the sound travels to the further microphone using trigonometry:
$$\text{Distance}=l\sin\theta$$

3. Equate the two expressions representing the same distance:
$$l\sin\theta=c\Delta t$$

4. Divide both sides by $l$ to isolate the angle expression:
$$\sin\theta=\frac{c\Delta t}{l}$$

**R.1.2 (3 points)** Find the expression to determine the velocity of a target from the pulse duration difference of a radar sensor. Derive the equations shown in the slides of Lecture 3 step by step.

1. Start with the base formula for the Doppler frequency shift $\Delta f$ given the emitted frequency $f_0$:
$$\Delta f=\frac{2\Delta v}{c}f_0$$

2. Multiply both sides by the wave propagation speed $c$:
$$c\Delta f=2\Delta vf_0$$

3. Divide both sides by $2f_0$ to isolate the velocity variable $\Delta v$:
$$\Delta v=\frac{c\Delta f}{2f_0}$$

**R.1.3 (1 point)** How can we measure the distance to a target?

We can measure distance using the time-of-flight principle by calculating the time delay between an emitted signal and its returning echo

**R.1.4 (1 point)** How can we measure the speed of a moving target?

We can measure the speed of a moving target by using the Doppler effect to analyze the frequency shift between an emitted wave and its returning echo.

## 2 Fast Fourier Transform (8 points)

### Tasks

**T.2.1** Create a signal consisting of the sum of two sine waves using a sample frequency of 1000Hz, one with amplitude of 1 and frequency of 50 Hz and the other with amplitude 0.5 and frequency 120 Hz. Plot the signal over a time slot of 2s.

```python
# type here the code...
```

![Figure](img/T2_1.png)

**T.2.2** Run a FFT (Fast Fourier transform) on the signal from T.2.1 and plot it. Normalize the output to 1 and only show positive frequencies.

```python
# type here the code...
```

![Figure](img/T2_2.png)

**T.2.3** Add random noise to the signal from T.2.1 and plot the signal again.

```python
# type here the code...
```

![Figure](img/T2_3.png)

**T.2.4** Run the FFT on the noisy signal from T.2.3 and plot it.

```python
# type here the code...
```

![Figure](img/T2_4.png)

### Report

**R2.1 (2 points)** Is it possible to implement FFT to an online data streaming? Why?

```text
Type here the answer...
```

**R2.2 (2 points)** How can you use FFT in signal processing?

```text
Type here the answer...
```

**R2.3 (2 points)** Deliver the code used to generate the signals and plots?

[See code ↗](code/Tutorial_5.ipynb)

## 3 Audio Correlation (8 points)

### Tasks

**T.3.1** Load the ‘chimes.wav’ file into the workspace and isolate one of its channels.

- Plot the signal with a reasonable time scale.
- If you have speakers/headphones: try to output the audio signal.

```python
### IMPORT THE AUDIO FILE ###
from scipy.io import wavfile

# Load the audio file
sample_rate, data = wavfile.read('../audio/chimes.wav')

# Isolate one channel
if len(data.shape) > 1:
    signal = data[:, 0] # Left channel
else:
    signal = data       # Already mono

### PLOT THE AUDIO SIGNAL ###
time = np.arange(len(signal)) / sample_rate

plt.plot(time, signal, color='b')
plt.title('Chimes Audio Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.xlim(0, time[-1])  # Limits the x-axis to the exact length of the audio
plt.show()
```

![Figure](img/T3_1.png)

**T.3.2** Run an FFT on the audio signal from T.3.1 and plot it.

```python
### RUN THE FFT ###
n = len(signal)

fft_output = np.fft.fft(signal)

frequencies = np.fft.fftfreq(n, 1 / sample_rate) # Calculate the frequencies corresponding to the FFT points
magnitude = np.abs(fft_output) # Take the absolute value to get the magnitude spectrum
magnitude_normalized = magnitude / np.max(magnitude) # Normalize the output to 1
# Filter out only the positive frequencies
positive_frequencies = frequencies[:n // 2]
positive_magnitude = magnitude_normalized[:n // 2]

### PLOT THE FFT SPECTRUM ###
plt.plot(positive_frequencies, positive_magnitude, color='r')
plt.title('Normalized FFT Spectrum')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Normalized Magnitude')
plt.grid(True)
plt.xlim(0, 5000)  # Zoomed into 0-5kHz where most audio frequencies lie
plt.show()
```

![Figure](img/T3_2.png)

**T.3.3** Generate a left and a right channel from the signal of T.3.1 and add a delay and scaling factor to one of them. Make the delay and scaling factors variable.

```python
delay = 0.0005  # seconds
scaling_factor = 0.7

# Convert the time delay into the number of discrete samples
delay_samples = int(delay * sample_rate)

# Left channel: Pad with zeros at the end
left_channel = np.pad(signal, (0, delay_samples), mode='constant')
# Right channel: Pad with zeros at the start
right_channel = np.pad(signal, (delay_samples, 0), mode='constant') * scaling_factor
```

**T.3.4** Plot the two signals in the same figure.

```python
time_padded = np.arange(len(left_channel)) / sample_rate

# Plot both signals together
plt.plot(time_padded, left_channel, label='Left Channel', color='b')
plt.plot(time_padded, right_channel, label='Right Channel', color='r')

plt.title('Left and Right Channels')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()
```

![Figure](img/T3_4.png)

**T.3.5** If you have speakers/headphones: listen to the signals and find parameters at which stereo localization works for you.

```python
# Stack channels vertically to create a stereo layout (2, N) and transpose to (N, 2)
stereo_signal = np.vstack((left_channel, right_channel)).T

# Ensure the data type is correct for audio playback (16-bit PCM integer)
if stereo_signal.dtype != np.int16:
    stereo_signal = (stereo_signal / np.max(np.abs(stereo_signal)) * 32767).astype(np.int16)

# Save the file into the audio directory with the delay value in the name
filename = f'../audio/chimes_stereo_{delay}.wav'
wavfile.write(filename, sample_rate, stereo_signal)
```

**T.3.6** Run cross-correlation on both signals and plot the correlation against delay.

```python
cross_corr = np.correlate(right_channel, left_channel, mode='full')

num_lags = len(cross_corr)
lags_samples = np.arange(-num_lags // 2 + 1, num_lags // 2 + 1)

lags_seconds = lags_samples / sample_rate # Convert sample lags into time delays (seconds)

plt.plot(lags_seconds, cross_corr, color='b')
plt.title('Cross-correlation vs. Time delay')
plt.xlabel('Delay [s]')
plt.ylabel('Correlation magnitude')
plt.grid(True)
plt.show()

# Find and print the peak location
estimated_delay = lags_seconds[np.argmax(cross_corr)]
print(f"True physical delay configured: {delay} seconds")
print(f"Delay estimated by cross-correlation peak: {estimated_delay} seconds")
```

![Figure](img/T3_6.png)

**T.3.7** Add noise with a normal distribution to both channels.

```python
noise_level = 1000.0  

left_noise = np.random.normal(0, noise_level, size=left_channel.shape)
right_noise = np.random.normal(0, noise_level, size=right_channel.shape)

left_channel_noisy = left_channel + left_noise
right_channel_noisy = right_channel + right_noise
```

**T.3.8** Run cross-correlation on the noisy signals and plot.

```python
cross_corr_noisy = np.correlate(right_channel_noisy, left_channel_noisy, mode='full')

num_lags_noisy = len(cross_corr_noisy)
lags_samples_noisy = np.arange(-num_lags_noisy // 2 + 1, num_lags_noisy // 2 + 1)

lags_seconds_noisy = lags_samples_noisy / sample_rate # Convert sample lags into time delays (seconds)

plt.plot(lags_seconds_noisy, cross_corr_noisy, color='b')
plt.title('Cross-correlation vs. Time delay for noisy signals')
plt.xlabel('Delay [s]')
plt.ylabel('Correlation magnitude')
plt.grid(True)
plt.show()

# Find and print the peak location
estimated_delay_noisy = lags_seconds_noisy[np.argmax(cross_corr_noisy)]
print(f"True physical delay configured: {delay} seconds")
print(f"Delay estimated by noisy cross-correlation peak: {estimated_delay_noisy} seconds")
```

![Figure](img/T3_8.png)

### Report

**R.3.1 (2 point)** Is it possible to implement the cross-correlation to an online data streaming? Why?

```text
No. An online data stream runs forever. If we try to run a standard cross-correlation on it continuously, the size of our data arrays grows infinitely, becoming a computationally challenging problem.
```

**R.3.2 (2 point)** If you answered “no” to R.3.1, how would you work around to use it to identify the interaural time delay?

```text
A work around would be to use a sliding window approach: first we divide the continuous incoming audio stream into small buffers of fixed size, then we run the cross correlation only on these slices of data.
```

**R.3.3 (4 points)** Deliver the code to generate the signals and the plots (T.3.1 - T.3.8).

[See code ↗](code/Tutorial_5.ipynb)

## 4 Signal Filtering (33 points)

### Tasks

**T.4.1** Create a signal consisting of two sine waves, one with amplitude of 1 and a frequency of 50 Hz and one with amplitude 0.5 and frequency of 500 Hz using a sample frequency of 10,000 Hz.

```python
# type here the code...
```

**T.4.2** Plot the signal over a time slot of 0.1s.

```python
# type here the code...
```

![Figure](img/T4_2.png)

**T.4.3** Design an analog low-pass passive filter with a cut-off frequency of 50 Hz.

```text
Type here the answer...
```

**T.4.4** Design and implement a first order discrete low-pass filter with cut-off frequency of 50 Hz.

```python
# type here the code...
```

**T.4.5** Apply the filter from T.4.4 to the signal created in T.4.1. Plot again the signal after filtering.

```python
# type here the code...
```

![Figure](img/T4_5.png)

**T.4.6** Design an analog high-pass passive filter with a cut-off frequency of 500 Hz.

```text
Type here the answer...
```

**T.4.7** Design and implement a first order discrete high-pass filter with cut-off frequency of 500 Hz.

```python
# type here the code...
```

**T.4.8** Apply the filter from T.4.7 to the signal created in T.4.1. Plot again the signal after filtering.

```python
# type here the code...
```

![Figure](img/T4_8.png)

**T.4.9** Create another sine wave signal with a frequency of 1,000 Hz using a sample frequency of 10,000 Hz. Then, add it to the signal created in T.4.1.

```python
# type here the code...
```

**T.4.10** Design an analog band-pass active filter to recover the 500 Hz signal.

```text
Type here the answer...
```

**T.4.11** Design and implement a discrete band-pass filter to recover the 500 Hz signal from the superposed signal.

```python
# type here the code...
```

**T.4.12** Apply the filter from T.4.11 to the signal created in T.4.9. Plot again the signal after filtering.

```python
# type here the code...
```

![Figure](img/T4_12.png)

### Report

**R.4.1 (2 points)** Detail the design process of the filter in T.4.3. Draw the required circuit and calculate the value for the components step by step.

```text
Type here the answer...
```

![Figure](img/R4_1.png)

**R.4.2 (2 points)** Detail the design process of the filter in T.4.4. Derive the equation to implement the filter step by step on a data stream.

```text
Type here the answer...
```

**R.4.3 (2 points)** Detail the design process of the filter in T.4.6. Draw the required circuit and calculate the value for the components step by step.

```text
Type here the answer...
```

![Figure](img/R4_3.png)

**R.4.4 (2 points)** Detail the design process of the filter in T.4.7. Derive the equation to implement the filter step by step on a data stream.

```text
Type here the answer...
```

**R.4.5 (2 points)** Detail the design process of the filter in T.4.10. Draw the required circuit and calculate the value for the components step by step.

```text
Type here the answer...
```

![Figure](img/R4_5.png)

**R.4.6 (2 points)** Detail the design process of the filter in T.4.11. Derive the equation to implement the filter step by step on a data stream.

```text
Type here the answer...
```

**R.4.7 (2 point)** What is the difference between passive and active filters?

```text
Type here the answer...
```

**R.4.8 (2 point)** What is the difference between FIR and IIR filters?

```text
Type here the answer...
```

**R.4.9 (2 point)** What is the “order” of a discrete filter?

```text
Type here the answer...
```

**R.4.10 (2 point)** How could you implement a continuous-time filter in a robotic system?

```text
Type here the answer...
```

**R.4.11 (2 point)** How could you implement a discrete-time filter in a robotic system?

```text
Type here the answer...
```

**R.4.12 (3 point)** What are the advantages and disadvantages of analog and digital filters in robotic systems?

```text
Type here the answer...
```

**R.4.13 (2 point)** Is it possible to make a 1000 Hz Low-Pass filter in a digital system with a sampling rate of 1000 Hz?

```text
Type here the answer...
```

**R.4.14 (6 points)** Deliver the code to generate the signals and the plots (T.4.1 - T.4.12).

```python
# type here the code...
```
