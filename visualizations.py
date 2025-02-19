import random
import streamlit as st
import plotly.graph_objects as go
import time
from algorithms import insertion_sort, merge_sort, quicksort

# Initial default values
N = 32
min_val, max_val = 1, 100  # Renamed min and max to avoid conflict with built-in functions

def generate_new_list(n, min_v, max_v):
    return [random.randint(min_v, max_v) for _ in range(n)]

# Initialize session state values
if 'min' not in st.session_state:
    st.session_state.min = min_val

if 'max' not in st.session_state:
    st.session_state.max = max_val

if 'lst' not in st.session_state:
    st.session_state.lst = generate_new_list(N, min_val, max_val)

if 'sorting' not in st.session_state:
    st.session_state.sorting = False

if 'paused' not in st.session_state:
    st.session_state.paused = True

if "last_fig" not in st.session_state:
    st.session_state.last_fig = None

if 'algorithm' not in st.session_state:
    st.session_state.algorithm = 'Insertion Sort'
    st.session_state.algorithm_fct = insertion_sort(st.session_state.lst)

# Sidebar controls
with st.sidebar:
    st.header('Controls')

    algorithm = st.selectbox(
        'Choose sorting algorithm:',
        ("Insertion Sort", "Merge Sort", "Quicksort"),
    )

    if algorithm != st.session_state.algorithm:
        st.session_state.algorithm = algorithm
        if algorithm == 'Insertion Sort':
            st.session_state.algorithm_fct = insertion_sort(st.session_state.lst)
        elif algorithm == 'Merge Sort':
            st.session_state.algorithm_fct = merge_sort(st.session_state.lst)
        elif algorithm == 'Quicksort':  # Fixed incorrect elif condition
            st.session_state.algorithm_fct = quicksort(st.session_state.lst)

    # Slider for the list size (n)
    st.session_state.n = st.slider('Sample size', 1, 256, N)

    # Frame rate settings
    st.session_state.frame_rate = st.slider('Frame rate (updates per second)', 1, 250, 30)
    st.session_state.delay = 1.0 / st.session_state.frame_rate

    # Button to generate a new list
    if st.button('Generate new list'):
        st.session_state.lst = generate_new_list(st.session_state.n, st.session_state.min, st.session_state.max)
        st.session_state.sorting = False
        # Reset the sorting generator to use the new list
        if st.session_state.algorithm == 'Insertion Sort':
            st.session_state.algorithm_fct = insertion_sort(st.session_state.lst)
        elif st.session_state.algorithm == 'Merge Sort':
            st.session_state.algorithm_fct = merge_sort(st.session_state.lst)
        elif st.session_state.algorithm == 'Quicksort':
            st.session_state.algorithm_fct = quicksort(st.session_state.lst)

    # Button to start sorting
    if st.button('Start Sorting'):
        st.session_state.sorting = True
        st.session_state.paused = False

    # Button to pause or resume
    if st.button("Pause" if not st.session_state.paused else "Resume", disabled=not st.session_state.sorting):
        st.session_state.paused = not st.session_state.paused

    st.text(st.session_state)

st.title('Sorting Visualizer')
chart = st.empty()
i = 0

while st.session_state.sorting:
    if not st.session_state.paused:
        try:
            # Perform sorting and update chart in real-time
            array, colors = next(st.session_state.algorithm_fct)

            # Color bars based on sorting state
            bar_colors = ['blue'] * len(array)
            for idx, color in colors.items():
                bar_colors[idx] = color

            # Plot the current state of the sorting process
            fig = go.Figure(data=[go.Bar(
                x=list(range(len(array))),
                y=array,
                marker_color=bar_colors,
                text=array,
                textposition='outside'
            )])

            i += 1
            chart.plotly_chart(fig, use_container_width=True, key=st.session_state.algorithm + str(i))
            time.sleep(st.session_state.delay)

        except StopIteration:
            st.session_state.sorting = False  # End sorting when done

# Initial plot before sorting starts
if not st.session_state.sorting:
    fig = go.Figure(data=[go.Bar(
        x=list(range(len(st.session_state.lst))),
        y=st.session_state.lst,
        marker_color='blue'
    )])
    chart.plotly_chart(fig, use_container_width=True)
