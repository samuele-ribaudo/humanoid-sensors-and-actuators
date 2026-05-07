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

    high_byte = None

    while not exit_event.is_set():
        b = dev.read(1)
        if not b:
            continue
        size = dev.getQueueStatus()
        b += dev.read(size)
        
        for d in b:
            if high_byte is None:
                # AUTO-SYNC CHECK: 
                # The high byte of a 10-bit value can ONLY be 0, 1, 2, or 3.
                # If we see a number bigger than 3, we are out of sync. Drop it.
                if d <= 3:
                    high_byte = d
            else:
                low_byte = d
                
                # Combine the two bytes into a 16-bit integer
                value_10bit = (high_byte << 8) | low_byte
                
                # Append the combined 10-bit value to our plotting buffer
                data_buffer.append(value_10bit)
                
                # Reset high_byte to None to start waiting for the next pair
                high_byte = None

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
    ax.set_title("Real-Time ADC Plotter (10-bit)")
    ax.set_xlabel("Samples")
    ax.set_ylabel("ADC Value (10-bit)")
    
    # 10-bit ADC ranges from 0 to 1023. Set limits slightly wider for visibility.
    ax.set_ylim(-20, 1050)
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
