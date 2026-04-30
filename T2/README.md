# Humanoid Sensors and Actuators
## Group 5
| Name | Matr. # | Email |
|------|---------|-------|
| Samuele Ribaudo | 03821248 | samuele.ribaudo@tum.de |
| Hong Yan Jun  | 03813507 | go75kes@mytum.de |
| Alessandro Canalicchio | 03796273 | go73xix@mytum.de |
| Niklas Peter | 03812287 | n.peter@tum.de |
| Emile Gebrael | 03812968 | emile.gebrael@tum.de |

# Tutorial 2 - Part 1


Course Instructors: Dr. Florian Bergner
hsa-lecture.ics@xcit.tum.de

Summer Semester 2026

## Initial Setup (Before the Tutorial!)

### Clone the tutorial project
Clone the project and follow the instructions in the `readme.md` file:
```bash
git clone "https://gitlab.lrz.de/hsa/students/hsa_t2s1_ws.git"
```

The best is to setup the Dev Container with LTSpice, but you can also directly install LTSpice in Windows or MacOS.
You can find a short crash course on LTSpice in http://denethor.wlu.ca/ltspice/.

## Electronic Basics (80 points)
After the introduction of microcontrollers, and acquiring the skills to program them for different applications, we now have a look at basic electronic circuits that find their applications in sensing and actuation.

In this tutorial we will learn:
- How to simulate circuits with LTSpice
- How to simulate and calculate filter circuits
- How to simulate operational amplifier (op-amp) circuits

## 2 Getting started with LTSpice (10 points)
In this tutorial we will start simulating electronic circuits with LTSpice. LTSpice bases on the open source circuit simulator SPICE (Simulation Program with Integrated Circuit Emphasis). SPICE was developed at the Electronics Research Laboratory of the University of California, Berkeley and is nowadays still used in integrated circuit and board-level design to check circuit design and predict circuit behavior. LTSpice provides you with a GUI to minimize your effort of writing SPICE programs. Nevertheless, LTSpice still supports all the features of SPICE programs and LTSpice simulations can be combined with manually written SPICE programs.

Familiarize yourself with the basic editing, simulation and evaluation capabilities of LTSpice in these first tasks:
**T.2.1 (2 points)** Create a new schematic in LTSpice and store it in `hsa_t2s1_ws/src`. Add a 5 V voltage source and serially connect it to a 10 kΩ resistor and a 1 µF capacitor. Hand in the circuit `T2_1_RC_op.asc`.

![T2_1_RC_op](ltspice/png/T2_1_RC_op.png)

See [file](ltspice/T2_1_RC_op.asc) ↗

**T.2.2 (2 points)** Start a DC operation point (`.op`) simulation with the circuit of **T.2.1** and have a look at the currents and voltages. Do they make sense? Please elaborate and explain. Make sure that the circuit of **T.2.1** contains your updates.
```answer
Yes thie currents and voltages make sense to us. Since we are using a DC source, once the capacitor is fully charger it behaves as an oopen circuit, therefore the currents passing trough the resistor and capacitor should be 0 (or a value close to zero). Thanks to Ohm's law V = RI we can say that there is no loss in voltage at the different nodes of the circuits, therefore is correct to measure 5V everywhere.
```

**T.2.3 (6 points)** Start a transient simulation (`.tran`) and measure the voltage and the current at the capacitor.
- **(2 points)** Submit the circuit `T2_3_RC_tran.asc`, and the screenshot `T2_3_RC_tran.png` of the plot with the measured voltage and current.

![tran](img/T2_3_RC_tran.png)

- **(2 points)** Compare the calculated τ = RC and the measured time constant VC(τ) = Vmax(1 − e^−1) ≈ 63.2% Vmax. Specify both time constants. Do they match? Explain your observation.

```answer
τ = RC = 10kOhm * 1uF = 0.01s = 10 ms
on the plot we obtain the value of 3.16V, corresponding to 63.2% of 5V, at 10.0ms, wich correspond to the teoretical calculated value, giving a complete match. This is because the simulation follows exactly the exponential charging law. 
```
- **(2 points)** Plot the power consumption of the circuit over time (P= UI) in LTSpice. Submit the screenshot `T2_3_RC_P.png` of the plot.

![power](img/T2_3_RC_P.png)


## 3 Filter Circuits - Optional Bonus (20 points)
**T.3.1 (2 points)** Copy the circuit of **T.2.1**. Conduct a small signal AC behavior analysis (`.ac`) with an amplitude of 1 V from 0.01 Hz to 100 Hz. Submit the circuit `T3_1_RC_ac.asc` and the screenshot `T3_1_RC_ac.png` of the phase and amplitude plot.
![T3_1_RC_ac](ltspice/png/T3_1_RC_ac.png)

See [file](ltspice/T3_1_RC_ac.asc) ↗

![ac](img/T3_1_RC_ac.png)

### 3.1 Report (18 points)
**R.3.1 (4 points)** Derive the complex transfer function `H(jω) = Vout / Vin` of the filter. Use symbolic expressions and explain each sub-step. You will get points for the symbolic calculations. You will only get one point for the correct result.
```answer
Type here the answer...
```

**R.3.2 (4 points)** Derive the gain G(ω) = |H(jω)| of the filter. Use symbolic expressions and explaineach sub-step. You will get points for the symbolic calculations. You will only get one point for the correct result.
```answer
Type here the answer...
```

**R.3.3 (4 points)** Derive the phase shift φ(ω) = arg(x+jy) = arctan2(y,x) ≈ arctan(y/x) of the filter. Use symbolic expressions and explain each sub-step. You will get points for the symbolic calculations. You will only get one point for the correct result.
```answer
Type here the answer...
```

**R.3.4 (4 points)** Derive the −3 dB cutoff frequency fc = ωc/(2π) where the gain of the filter equals G(ω) = 1/√(2). Use symbolic expressions and explain each sub-step. You will get points for the symbolic calculations. You will only get one point for the correct result
```answer
Type here the answer...
```

**R.3.5 (2 points)** Compare your results with the result of your LTSpice simulation in **T.3.1**. Elaborate and explain your observations.
```answer
Type here the answer...
```

## 4 Operational Amplifier (Op-Amp) Circuits (18 points)
### 4.1 Voltage Divider with a Resistive Output Load (6 points)

**T.4.1 (1 point)** Create a voltage divider circuit with a 5 V voltage source in LTSpice. Set both resistor values of the voltage divider to 200 kΩ and connect a 500 kΩ load resistance on the divider’s output. Submit the circuit `T4_1_VD.asc`.

![T2_1_RC_op](ltspice/png/T4_1_VD.png)

See [file](ltspice/T4_1_VD.asc) ↗

**T.4.2 (1 point)** Increase the crosscurrent of the divider by lowering the divider’s resistor values. How does the load resistance influence the output voltage? Explain your observations and submit the circuit `T4_2_VD.asc`.
```answer
By lowering the divider resistors from 200kΩ to 20kΩ, the output voltage increased from 2.08V to 2.45V. Since the load is connected in parallel to the bottom resistor, with 200kΩ the load resistor significantly alters the total resistance of the bottom half because they are similar in magnitude.By lowering the divider resistors to 20kΩ the cross current of the divider increases, thus the 500kΩ resistor has a much smaller relative impact on the parallel resistance calculation.
```
![T2_1_RC_op](ltspice/png/T4_2_VD.png)

See [file](ltspice/T4_2_VD.asc) ↗

**T.4.3 (2 points)** How does the output voltage error (in %) changes for higher divider currents? Provide two examples and describe the tendency of the error. Explain your observations.
```answer
To measure the error we used the formula Error % = |2.5 - V_measured| / 2.5 * 100.

- With the 200kkΩ resistor we measured an output voltage of 2.08, leadig to an error of 16.8%
- With the 20kΩ resistor we measured an output voltage of 2.45, leading to an error of 2.0%

The tendency of the error is to decrease.
```

**T.4.4 (2 points)** What is the major drawback of high divider currents?
```answer
The major drawback of high divider currents is an high power consumption. This is due to the fact that the power is inversely proportional to the resistance of the circuit (P = V^2/R), and therefore lowering the overall resistance will lead to an higher power consumpion.
```

### 4.2 Voltage Divider with a Resistive Output Load and a Voltage Follower (8 points)

**T.4.5 (2 points)** Copy the circuit of **T.4.1** and add an op-amp based voltage follower circuit between the voltage divider and the resistive load. Include the `opamp` component library using the spice directive `.lib opamp.sub.` Both, the op-amp symbol and the component library are provided by LTSpice. Submit the circuit `T4_5_opamp.asc`.
```answer
Type here the answer...
```

![T4_5_opamp](ltspice/png/T4_5_opamp.png)

See [file](ltspice/T4_5_opamp.asc) ↗

**T.4.6 (2 points)** How does the output voltage changes in comparison to the setup of **T.4.1** without the voltage follower? Explain your observations.
```answer
Type here the answer...
```

**T.4.7 (4 points)** How much can the crosscurrent of the voltage divider be reduced without affecting the desired output voltage? Explain the limits and your observations.
```answer
Type here the answer...
```

### 4.3 Report (4 points)
**R.4.1 (4 points)** What are the advantages and disadvantages of very small crosscurrents in voltage dividers? Explain the advantages/disadvantages you have named.
```answer
Type here the answer...
```
