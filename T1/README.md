# Humanoid Sensors and Actuators  
# Tutorial 1 - Part 1

Course Instructors: Dr. Florian Bergner
hsa-lecture.ics@xcit.tum.de

Summer Semester 2026

## Initial Setup (Before the Tutorial!)

### Prepare PC

- Install one of the following operating systems:
  - Ubuntu 24.04 AMD64 (tested)
  - Ubuntu 22.04 AMD64 (supported)
  - Ubuntu 20.04 AMD64 (supported)

- We strongly recommend to have a native Ubuntu installation, we will not support a virtual machine, but you are free to use it
- Docker in Windows (WSL) or Docker in MacOS will NOT work
- If you do not have a native Ubuntu OS you can try to use VirtualBox
- We only support AMD64, ARM64 or other architectures (e.g. WIN ARM Surface, Apple M1, M2, M3 etc.) are NOT supported, even when running VirtualBox

### Install and Setup Docker

1. Uninstall old versions
2. Install using the apt repository (only steps 1 to 3, step 3: running the hello world image is optional)
3. Manage Docker as a non-root user

### Install and Setup VS Code

1. Install VS Code
2. https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

### Pull the Docker image

```bash
docker login "gitlab.lrz.de:5005"
docker pull "gitlab.lrz.de:5005/hsa/students/docker/avr/avr:focal-vscode"
docker tag "gitlab.lrz.de:5005/hsa/students/docker/avr/avr:focal-vscode" "avr:focal-vscode"
```

### Clone the tutorial project

```bash
git clone "https://gitlab.lrz.de/hsa/students/hsa_t1s1_ws.git"
```

### Install the udev rules for the programmer

We need to install `udev` rules on the Ubuntu OS to use the programmer without `sudo`. Open a Terminal and make sure you are in the tutorial project folder `hsa_t1s1_ws`.

```bash
cd hsa_t1s1_ws
sudo cp -v udev/97-ics-avr.rules /etc/udev/rules.d
sudo udevadm control --reload
```
If you have the programmer already connected you need to unplug and plug it.

### Open the tutorial project in the Dev Container

1. Remove any previously started Dev Containers of the project.
```bash
docker rm hsa_t1s1_ws_devcont
```
2. Open the tutorial project in VS Code:
```bash
cd hsa_t1s1_ws
code .
```
3. Press `Ctrl+Shift+P`, type `Dev Containers: Rebuild and Reopen In Container`, and press `Enter`. The project is now opened in the Dev Container and all terminals in VS Code will be running in the container environment.

4. After you built the Dev Container you can also open it later again with `Dev Containers: Reopen In Container` and skip the container building process.

## Oscilloscope

During our tutorials we will be using an oscilloscope to measure the analog signals of the microcontroller, if you are unfamiliar with oscilloscopes, research on oscilloscope basics. We recommend these tutorials as a good starting point:
https://learn.sparkfun.com/tutorials/how-to-use-an-oscilloscope/all

## Microcontrollers (MCUs): Introduction
In this first part of tutorial 1 we will learn:
- How to write and compile assembly and C code for the AVR MCU
- How to use the general purpose IO pins of AVR MCUs

## 1 Microcontroller Circuit (6 points)

### 1.1 Report (6 points)

**R.1.1(2 points)** What are decoupling capacitors? Please explain in detail why they are needed in circuits with MCUs.
```answer
type here the answer...
```
**R.1.2 (2 points)** What properties are important for good decoupling capacitors? Name at least two and explain.
```answer
type here the answer...
```
**R.1.3 (2 points)** Where would you place decoupling capacitors in a PCB layout. Explain why you would place them there.
```answer
type here the answer...
```
## 2 Programming the microcontroller: (9 points)

### 2.1 Finalize setup for programming the real AVR

You already installed all the required programs in the previous steps. Connect your board to your computer and finalize the setup with the following steps:

1. Open the tutorial project in VS Code:
```bash
cd hsa_t1s1_ws
code.
```
2. Press `Ctrl+Shift+P`, type `Dev Containers: Reopen In Container`, and press `Enter`.
   
3. Check if the connection to the AVR microcontroller is fine:
```bash
# read fuse bits (Default: lfuse=0xE1, hfuse=0x99): JTAG on, 1 MHz, internal clock
avrdude -c avrispmkII -P usb B10 -p atmega32 -n -U lfuse:r:-:b -U hfuse:r:-:b
```
4. Make sure that the AVR microcontroller has the correct settings:
```bash
# write fuse bits: JTAG off, internal clock @ 1 MHz: lfuse=0xE1, hfuse=0xC9
avrdude -c avrispmkII -P usb B10 -p atmega32 -U lfuse:w:0xE1:m -U hfuse:w:0xC9:m
```
5. *Optional*: Other fuse bit setting for higher CPU frequencies (Skip for now)
```bash
# write fuse bits: JTAG off, internal clock @ 1 MHz: lfuse=0xE1, hfuse=0xC9
avrdude -c avrispmkII -P usb B10 -p atmega32 -U lfuse:w:0xE1:m -U hfuse:w:0xC9:m
# write fuse bits: JTAG off, internal clock @ 2 MHz: lfuse=0xE2, hfuse=0xC9
avrdude -c avrispmkII -P usb B10 -p atmega32 -U lfuse:w:0xE2:m -U hfuse:w:0xC9:m
# write fuse bits: JTAG off, internal clock @ 4 MHz: lfuse=0xE3, hfuse=0xC9
avrdude -c avrispmkII -P usb B10 -p atmega32 -U lfuse:w:0xE3:m -U hfuse:w:0xC9:m
# write fuse bits: JTAG off, internal clock @ 8 MHz: lfuse=0xE4, hfuse=0xC9
avrdude -c avrispmkII -P usb B10 -p atmega32 -U lfuse:w:0xE4:m -U hfuse:w:0xC9:m
```

### 2.2 How to program your microcontroller
After building your project, a .hex file is generated inside the build folder of your project. This file is the one that we need to flash to our microcontroller.

- To manually flash a `.hex` file to the microcontroller, run in a terminal inside the folder where the `.hex` file is:
```bash
cd hex
# flash the program blink.hex
avrdude -c avrispmkII -P usb B10 -p atmega32 -U flash:w:blink.hex
```
- After building you can also execute the make target `prog_<app-name>`:
```bash
cd hsa_t1s1_ws
mkdir -p build
cd build
cmake..
make
make prog_asm_blink
```

- To manually erase the microcontroller:
```bash
avrdude -c avrispmkII -P usb B10 -p atmega32 -e
```

### 2.3 Blinking a LED (9 points)
1. Program the microcontroller using the `.hex` file. You should see one LED blinking.
```bash
cd hsa_t1s1_ws
cd hex
# flash the program blink.hex
avrdude -c avrispmkII -P usb B10 -p atmega32 -U flash:w:blink.hex
```
**T.2.1 (2 points)** Use the oscilloscope to measure the pin `PC0` (Remember to connect it between the LED and ground (GND)). Configure your oscilloscope to have 2V/div and 500.00ms/div. Submit a picture of it named `blink_trace.png`
```answer
type here the answer...
```
**R.2.1 (2 points)** Your oscilloscope has different trigger modes. What do the different trigger modes mean? What does the trigger level and source mean?
```answer
type here the answer...
```
**R.2.2 (2 points)** Your oscilloscope has also different sweep types. Explain the different sweep types and their use cases.
```answer
type here the answer...
```
**R.2.3 (3 points)** What happens when you change the trigger mode in your reading from T2.1? When do you change the slope type? When do you change the sweep type? What is the best trigger configuration for this reading? Explain why.
```answer
type here the answer...
```
## 3 Using the GPIO Peripherial Block (60 points)

### 3.1 Setting Pin Levels in Assembly (20 points)
Please use the tutorial project `hsa_t1s1_ws` as basis for the tasks introduced in this section.
Please submit the code you created as specified in the tasks.
You can find template files for each task in the folder `hsa_t1s1_ws/src/gpio_asm/src/applications`.
For this tutorial you will need to use the documentation of the AVR microcontroller that we are using.
You can find it in the folder `hsa_t1s1_ws/docs`.

**T.3.1 (4 points)** Write an assembly program which lets the LED on `PORTC` on pin `PC0` blink.
The LED should stay on for one second and stay off for one second. Please use the code fragment of `Listing 1` to generate a delay of one second.
You submit the file `main_asm_blink.S` which contains the main function of your assembly program and your solution for this task.
```asm
; wait for one second
    ldi r18, 0x3F
    ldi r24, 0x0D
    ldi r25, 0x03
1:  subi r18, 0x01
    sbci r24, 0x00
    sbci r25, 0x00
    brne 1b        ; local label backward
    rjmp 1f        ; local label forward
1:  nop
```
**T.3.2 (2 points)** Your program of T.3.1 avoids changing the bits of other pins on `PORTC`.
```asm
type code here...
```

**T.3.3 (4 points)** Write an assembly program which turns the three LEDs on pins `PC0`, `PC1`, and `PC2` on and off with a delay of one second continuously in the following sequence:
    
    Step 1 : PC0 on, PC1 off, PC2 off
    Step 2 : PC0 off, PC1 on, PC2 off
    Step 3 : PC0 off, PC1 off, PC2 on

You submit the file `main_asm_blink3.S` which contains the main function of your assembly program and your solution for this task.
```asm
type code here...
```
**T.3.4 (Bonus) (4 points)** Using your oscilloscope visualize the three signals at the same time (using three different channels).
Submit a picture of it named `blink3_trace.png`

**T.3.5 (2 points)** Your program of **T.3.3** avoids changing the bits of other pins on `PORTC`.

**T.3.6 (4 points)** Find the most efficient set of assembly instructions such that changing the pin levels in each step of T.3.3 only takes in sum 4 CPU cycles.
You will get only points if your set of instructions does not manipulate the bits of other pins on `PORTC`.
You submit the file `main_asm_blink3eff.S` which contains the main function of your assembly program and your solution for this task.
Please add comments to your code why you believe that your set of instructions only takes 4 CPU cycles.
```asm
type code here...
```

## 3.2 Setting Pin Levels in C (6 points)
Please use the tutorial project `hsa_t1s1_ws` as basis for the tasks introduced in this section.
Please submit the code you created as specified in the tasks.
You can find template files for each task in the folder `hsa_t1s1_ws/src/gpio_c/src/applications`.

**T.3.7 (2 points)** Implement **T.3.1** using C code. You submit the file `main_blink.c` which contains the main function of your program and your solution for this task.
```c
type code here...
```

**T.3.8 (1 point)** Your program of **T.3.7** avoids changing the bits of other pins on `PORTC`.

**T.3.9 (2 points)** Implement **T.3.3** using C code. You submit the file `main_blink3.c` which contains the main function of your program and your solution for this task.
```c
type code here...
```

**T.3.10 (1 point)** Your program of **T.3.9** avoids changing the bits of other pins on `PORTC`.

## 3.3 Reading Pin Levels in Assembly and C (8 points)
Please use the respective template files introduced in the previous sections as basis for the following tasks.

**T.3.11 (4 points)** Write an assembly program that mirrors (copies) the input of pin `PC4` to pin `PC3`. Delay the input by one second using the delay code of `Listing 1`. You submit the file `main_asm_mirror.S` which contains the main function of your program and your solution for this task.
```asm
type code here...
```

**T.3.12 (1 point)** Your program of **T.3.11** avoids changing the bits of other pins on `PORTC`.

**T.3.13 (2 points)** Implement **T.3.11** using C code. You submit the file `main_mirror.c` which contains the main function of your program and your solution for this task.
```c
type code here...
```

**T.3.14 (1 point)** Your program of **T.3.13** avoids changing the bits of other pins on `PORTC`.

## 3.4 Report (26 points)

**R.3.1 (4 points)** How can you ensure that the logic levels of 4 pins are changed at exactly the same time without changing the other pins on the port? Provide an example in assembly code where you set the two pins `PC0` and `PC1` to high and the two pins `PC2` and `PC3` to low at the same time (CPU cycle).
```answer
type here the answer...
```

**R.3.2 (2 points)** Can you change the logic level of 2 pins of 2 different ports at the same time? Justify your answer by providing an example.
```answer
type here the answer...
```

**R.3.3 (6 points)** Explain each line of assembly code in `Listing 1`. For each correct explanation you get a point for lines 2-3, line 4, lines 6-7, line 8, line 9, and line 10.
```answer
type here the answer...
```

**R.3.4 (4 points)** Explain and calculate why the code fragment of `Listing 1` takes exactly (not approximately) one second when the CPU is running at 1 MHz.
```answer
type here the answer...
```

**R.3.5 (1 point)** What are the main disadvantages of busy waiting, even when we can achieve delays with very high accuracy?
```answer
type here the answer...
```

**R.3.6 (1 point)** In **R.3.4** you calculated that the code fragment of `Listing 1` takes exactly one second when the CPU is running at 1 MHz. However, in certain cases this code fragment will consume more CPU cycles than calculated in *R.3.4*. Please explain when this is the case.
```answer
type here the answer...
```

**R.3.7 (1 point)** Why does the MCU implement two address spaces for data and registers and two sets of assembly instructions (IN/OUT and LD/ST) to access these address spaces? Please explain and justify your answer.
```answer
type here the answer...
```

**R.3.8 (1 point)** Provide an example where you once use OUT and then ST to write the value `0xAC` to the peripheral register `PORTD`. Please look up the addresses of `PORTD` in the datasheet of the MCU.
```answer
type here the answer...
```

**R.3.9 (2 points)** How many CPU cycles are needed to load the address of PORTD and then write the value `0xAC` to the register `PORTD` when using OUT and when using ST?
```answer
type here the answer...
```

**R.3.10 (4 points)** Given a peripheral register with an address `0x15`, how can you create a variable in C that allows you to read/write this register without using the device support headers? (Hint: You will need to use type conversions.)
```answer
type here the answer...
```
