#!/usr/bin/python3

import sys
import json
import threading
import collections

import ftd2xx
import ftdi_tools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configure how many data points to show on the screen at once
MAX_POINTS = 500
# Deque is thread-safe for appends and automatically drops old items
data_buffer = collections.deque([0] * MAX_POINTS, maxlen=MAX_POINTS)

def read_ftdi_thread(
        dev: ftd2xx.FTD2XX, 
        exit_event: threading.Event):
    
    dev.setTimeouts(200, 0)
    print("Reading thread started...")

    while not exit_event.is_set():
        b = dev.read(1)
        if not b:
            continue
        size = dev.getQueueStatus()
        b += dev.read(size)
        
        # Append the raw byte values (0-255) to our plotting buffer
        for d in b:
            data_buffer.append(d)

    print("Exit reading thread...")

# Matplotlib animation update function
def update_plot(frame, line):
    line.set_ydata(data_buffer)
    return line,

if __name__ == '__main__':

    ftdiVer = ftdi_tools.getLibraryVersionString()
    print(f"FTDI library version: {ftdiVer}")

    print("Detected FTDI devices:")
    dl = ftdi_tools.getDeviceInfoList()
    print(json.dumps(dl, indent=4))

    dev_num = None
    for ind, d in enumerate(dl):
        if d['description'] == "SkinCellAdapter":
            dev_num = ind
            break

    if dev_num is None:
        print("Error: SkinCellAdapter not found.")
        exit(1)

    # Setup FTDI Device (matching log.py settings)
    dev = ftd2xx.open(dev_num)
    dev.setBaudRate(62500)
    dev.setLatencyTimer(2)
    ftdi_tools.flushRx(dev)

    # Event to signal the thread to shut down cleanly
    exit_event = threading.Event()
    
    # Start the background data collection thread
    thread = threading.Thread(target=read_ftdi_thread, args=(dev, exit_event))
    thread.daemon = True
    thread.start()

    # Setup Matplotlib Figure
    fig, ax = plt.subplots()
    ax.set_title("Real-Time ADC Plotter")
    ax.set_xlabel("Samples")
    ax.set_ylabel("ADC Value (8-bit)")
    
    # 8-bit ADC ranges from 0 to 255. Set limits slightly wider for visibility.
    ax.set_ylim(-5, 260)
    ax.set_xlim(0, MAX_POINTS)
    
    # Initialize an empty line
    line, = ax.plot(range(MAX_POINTS), data_buffer, color='blue')

    # Create the animation that updates every 50 ms
    ani = animation.FuncAnimation(
        fig, update_plot, fargs=(line,), interval=50, blit=True, cache_frame_data=False
    )

    print("Starting real-time plot. Close the plot window to exit.")
    
    try:
        # plt.show() blocks execution until the window is closed
        plt.show()
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping script...")
        exit_event.set()
        thread.join(timeout=2.0)
        dev.close()
        print("Stopped.")
        exit(0)
