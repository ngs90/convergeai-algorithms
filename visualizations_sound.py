import random
import streamlit as st
import plotly.graph_objects as go
import time
import numpy as np
from algorithms import insertion_sort
import io
import wave

# initial default values
N = 32
min, max = 1, 100

def generate_new_list(n, min, max):
    return [random.randint(min, max) for x in range(0, n)]

# Function to generate a sine wave for the sound
def generate_sine_wave(frequency, duration=0.2, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio_data = np.sin(2 * np.pi * frequency * t)
    audio_data = (audio_data * 32767).astype(np.int16)  # Convert to 16-bit PCM format
    return audio_data

# Function to play the sound in Streamlit
def play_sound(frequency):
    audio_data = generate_sine_wave(frequency)
    
    # Create a WAV file from the generated sound
    byte_io = io.BytesIO()
    with wave.open(byte_io, 'wb') as wave_file:
        wave_file.setnchannels(1)
        wave_file.setsampwidth(2)  # 2 bytes for 16-bit audio
        wave_file.setframerate(44100)
        wave_file.writeframes(audio_data.tobytes())
    
    byte_io.seek(0)
    st.audio(byte_io, format='audio/wav')

# Initialize session state values
if 'min' not in st.session_state:
    st.session_state.min = min

if 'max' not in st.session_state:
    st.session_state.max = max

if 'lst' not in st.session_state:
    st.session_state.lst = generate_new_list(N, min, max)

if 'sorting' not in st.session_state:
    st.session_state.sorting = False

if 'paused' not in st.session_state:
    st.session_state.paused = True

if "last_fig" not in st.session_state:  # Stores last rendered figure
    st.session_state.last_fig = None

# Sidebar controls
with st.sidebar:

    # Slider for the list size (n)
    st.session_state.n = st.slider('Sample size', 1, 256, N)
    
    st.header('Controls')

    # Frame rate settings
    st.session_state.frame_rate = st.slider('Frame rate (updates per second)', 1, 250, 30)
    st.session_state.delay =  1.0 / st.session_state.frame_rate

    # Button to generate a new list based on updated n
    if st.button('Generate new list'):
        st.session_state.lst = generate_new_list(st.session_state.n, st.session_state.min, st.session_state.max)
        st.session_state.sorting = False

    # Button to start sorting
    if st.button('Start Sorting'):
        st.session_state.sorting = True
        st.session_state.paused = False

    # Button to pause or resume
    if st.button("Pause" if not st.session_state.paused else "Resume", disabled=not st.session_state.sorting):
        st.session_state.paused = not st.session_state.paused

    st.text(st.session_state)

# Create the sorting generator when the list is changed
generator = insertion_sort(st.session_state.lst)

st.title('Sorting Visualizer')
chart = st.empty()

# Store last frequency to smoothly transition between values
last_frequency = None

while st.session_state.sorting:
    if not st.session_state.paused:
        try:
            # Perform sorting and update chart in real-time
            array, colors = next(generator)

            # Color bars based on sorting state
            bar_colors = ['blue'] * len(array)
            for idx, color in colors.items():
                bar_colors[idx] = color

            # Check if there is a green or red bar and play sound accordingly
            green_bar_index = None
            red_bar_index = None
            for idx, color in colors.items():
                if color == 'green':
                    green_bar_index = idx
                if color == 'red':
                    red_bar_index = idx

            # If green bar found, calculate frequency and play sound smoothly
            if green_bar_index is not None:
                bar_value = array[green_bar_index]
                frequency = 440 + (bar_value - 1) * 2  # Frequency increases with the value of the bar

                # Smooth the frequency change
                if last_frequency is None:
                    last_frequency = frequency
                else:
                    frequency = last_frequency + (frequency - last_frequency) * 0.1  # Gradual transition
                last_frequency = frequency

                play_sound(frequency)
            
            # If red bar found, calculate frequency and play sound smoothly
            if red_bar_index is not None:
                bar_value = array[red_bar_index]
                frequency = 300 + (bar_value - 1) * (2000 - 300) / 99  # Scale between 300 Hz to 2000 Hz

                # Smooth the frequency change
                if last_frequency is None:
                    last_frequency = frequency
                else:
                    frequency = last_frequency + (frequency - last_frequency) * 0.1  # Gradual transition
                last_frequency = frequency

                play_sound(frequency)

            # Plot the current state of the sorting process
            fig = go.Figure(data=[go.Bar(
                x=list(range(len(array))), 
                y=array, 
                marker_color=bar_colors,
                text=array,  # Add text (the value of each bar)
                textposition='outside'  # Position the text on top of the bars
            )])
            chart.plotly_chart(fig, use_container_width=True)

            time.sleep(st.session_state.delay)

        except StopIteration:
            st.session_state.sorting = False  # End sorting when done

# Initial plot before sorting starts
if not st.session_state.sorting:
    fig = go.Figure(data=[go.Bar(
        x=list(range(len(st.session_state.lst))), 
        y=st.session_state.lst, 
        marker_color='blue',
        text=st.session_state.lst,  # Add text (the value of each bar)
        textposition='outside'  # Position the text on top of the bars
    )])
    chart.plotly_chart(fig, use_container_width=True)
