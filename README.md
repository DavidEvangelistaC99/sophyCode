# Pulse Compression of Chirp Signals for Weather Radar

<p align="center">
  <img src="images/sophy.jpg" width="900">
</p>

<p align="center">
  <em>SOPHy weather radar at the Radio Observatory of Jicamarca (ROJ).</em>
</p>

## Overview
This repository contains waveform generation, data acquisition, and signal
processing algorithms developed during my undergraduate thesis at the
**Radio Observatory of Jicamarca (ROJ)**. The work focuses on **chirp-based
pulse compression** techniques to improve signal-to-noise ratio (SNR) in
meteorological radar systems.

The implemented framework integrates **USRP-based transmission and reception**
(adapted from MIT Haystack’s DigitalRF tools) with post-processing algorithms
based on the **ROJ Signal Chain library**, and is validated using real radar
data from the SOPHy weather radar.

## Scientific Context
Pulse compression is a key technique in modern solid-state weather radars,
allowing high sensitivity without sacrificing range resolution. Linear FM
(chirp) waveforms are particularly attractive due to their robustness and
processing gain when combined with matched filtering and Doppler processing.

## Methods
- Linear FM (chirp) waveform generation
- USRP-based transmission and reception
- Matched filtering and pulse compression
- Doppler spectrum analysis
- SNR estimation over azimuth angles
- Pulse Pair processing for radar moment estimation

## Results
- Approximately **13 dB average SNR improvement** compared to complementary codes
- Validation using **real data from the SOPHy weather radar**
- Generation of PPI products including reflectivity, radial velocity,
  spectral width, and polarimetric variables

## Repository Structure
- `tx/`: Waveform generation and transmission scripts using a USRP platform  
  (adapted from MIT Haystack DigitalRF; includes chirp waveform generation)
- `rx/`: USRP-based data acquisition scripts adapted from DigitalRF, storing
  received data in HDF5 format
- `processing/`: Signal processing scripts based on the ROJ Signal Chain library,
  including Doppler spectrum estimation and PPI generation using Pulse Pair
- `results/`: PPI plots, Doppler spectra, and animated radar products
- `schain/`: Signal processing library developed by the Radio Observatory of
  Jicamarca (ROJ)
- `legacy/`: Early exploratory scripts and development drafts
- `test/`: Scripts and auxiliary files used during thesis data acquisition

## Requirements
- Python 3.10+
- NumPy
- SciPy
- Matplotlib
- digital_rf
- ROJ Signal Chain library (`schain`)

## References
1. Sebastián V. P., *GNURADIO_CHIRP*: Open-source implementation of chirp-based
   radar waveforms and pulse compression techniques.  
   https://github.com/sebastianVP/GNURADIO_CHIRP

2. MIT Haystack Observatory, *DigitalRF*: A flexible framework for RF signal
   recording and playback widely used in radar and radio science applications.  
   https://github.com/MITHaystack/digital_rf

3. Radio Observatory of Jicamarca (ROJ), *Real-time weather radar products*.  
   https://www.igp.gob.pe/observatorios/radio-observatorio-jicamarca/realtime/plot/400/reflectivity/

## Author
**David Fernando Evangelista Cuti**  
B.Sc. Electronic Engineering – National University of Engineering (UNI), Peru

