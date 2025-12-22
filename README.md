![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEj1rei20Yq1QULcdF6_aFv3heVCIHSX3g9W0pR71ZyLcfKOK4mdv2vHo-o2CrznyekA2ireoj22rMkQACvKLio_Z13SyShnP4JRxrkNPwUpYWNUPtnEmS18knp__HwLOFb_NmSo7QUNABkl4vjbXE5GMS7FzNNJy0xXIna5zC6EcPNPdNxQyd74Bw8rtQ/s1880/RTSpecAn_Fig1.PNG)


## Descripción

En este repositorio se encuentran los scripts que se fueron avanzando para la generación de la señal *Chirp*. Se busca la mejora de la sensibilidad y resolución del radar *SOPHy*.

## Referencias

1. https://github.com/sebastianVP/GNURADIO_CHIRP 
2. https://github.com/MITHaystack/digital_rf

# Pulse Compression of Chirp Signals for Weather Radar

## Overview
This repository contains signal processing algorithms developed during my
undergraduate thesis at the Radio Observatory of Jicamarca (ROJ), focused on
chirp-based pulse compression to improve SNR in meteorological radar systems.

## Scientific Context
Pulse compression is essential in modern solid-state weather radars to achieve
high sensitivity without sacrificing range resolution.

## Methods
- Linear FM (chirp) waveform generation
- Matched filtering
- Doppler spectrum analysis
- SNR estimation over azimuth angles

## Results
- ~13 dB average SNR improvement compared to complementary codes
- Validated using real radar data from weather radar SOPHy 

## Repository Structure
- `legacy/`: early exploratory codes
- `signal_processing/`: core algorithms
- `radar/`: radar-specific simulations and analysis
- `schain/`: signal processing library developed by the Radio Observatory of Jicamarca (ROJ).

## Requirements
Python 3.10+, NumPy, SciPy, Matplotlib

## Author
David Fernando Evangelista Cuti  
B.Sc. Electronic Engineering – UNI, Peru
