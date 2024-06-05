"""
Script to create word-level boundaries for each word in a Praat TextGrid file.
"""
import os
import numpy as np
import soundfile as sf
from praatio import tgio

## loop through all files in the directory
for filename in os.listdir("../data/nasal"):
    # Load the audio file
    filename = filename.split(".")[0]
    idu_name = filename.split("__")[1]
    audio_file = "../data/nasal/" + filename + ".wav"

    # Get WAV file info
    # wav_info = sf.info(wav_path)
    data, samplerate = sf.read(audio_file)

    # Define silence threshold and minimum silence duration
    silence_thresh = 0.05  # adjust this value as needed
    min_silence_duration = 0.1  # in seconds

    # Convert minimum silence duration to number of samples
    min_silence_samples = int(min_silence_duration * samplerate)

    # Find silence regions
    silence_starts = []
    silence_ends = []
    in_silence = False
    silence_start = 0

    for i in range(len(data)):
        if not in_silence and abs(data[i]) < silence_thresh:
            in_silence = True
            silence_start = i
        elif in_silence and abs(data[i]) >= silence_thresh:
            in_silence = False
            if i - silence_start >= min_silence_samples:
                silence_starts.append(silence_start)
                silence_ends.append(i)

    # Remove silence regions
    non_silent_data = []
    prev_end = 0
    non_silent_intervals = []

    for start, end in zip(silence_starts, silence_ends):
        non_silent_data.extend(data[prev_end:start])
        non_silent_intervals.append((prev_end / samplerate, start / samplerate))
        prev_end = end

    non_silent_data.extend(data[prev_end:])
    non_silent_intervals.append((prev_end / samplerate, len(data) / samplerate))
    # Convert non-silent data to numpy array
    non_silent_data = np.array(non_silent_data)


    print("Start and end times of non-silent regions (in seconds):")
    for start_time, end_time in non_silent_intervals:
        start_time = round(start_time, 2)
        end_time = round(end_time, 2)

    # Calculate the duration of non-silent data
    duration = len(non_silent_data) / samplerate
    print(f"Duration of non-silent data: {duration:.2f} seconds")

    # Create a new TextGrid
    textgrid = tgio.Textgrid()

    # Create the entry list for the IntervalTier
    entries = [(start_time, duration, idu_name)]

    # Create the IntervalTier with the entry list
    word_tier = tgio.IntervalTier(name="words", entryList=entries)

    # Add the IntervalTier to the TextGrid
    textgrid.addTier(word_tier)

    # Save the TextGrid
    textgrid.save("../data/original_nasal_textgrids/" + filename + ".TextGrid")
