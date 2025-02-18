import random
import streamlit as st
import plotly.graph_objects as go
import time
from algorithms import insertion_sort

# initial default values
N = 32
min, max = 1, 100

def generate_new_list(n, min, max):
    return [random.randint(min, max) for x in range(0, n)]

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

while st.session_state.sorting:
    if not st.session_state.paused:
        try:
            # Perform sorting and update chart in real-time
            array, colors = next(generator)

            # Color bars based on sorting state
            bar_colors = ['blue'] * len(array)
            for idx, color in colors.items():
                bar_colors[idx] = color

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
    fig = go.Figure(data=[go.Bar(x=list(range(len(st.session_state.lst))), y=st.session_state.lst, marker_color='blue')])
    chart.plotly_chart(fig, use_container_width=True)