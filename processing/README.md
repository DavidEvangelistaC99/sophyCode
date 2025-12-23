## Signal Processing Scripts

This folder contains the main signal processing scripts used to analyze
the radar data collected during the SOPHy experiments. All processing routines rely on the **Signal Chain library** developed by the
**Radio Observatory of Jicamarca (ROJ)**, which provides core tools for radar
signal processing and analysis.

It includes:

- `sophy_test.py`: Frequency-domain signal processing script used to compute
  Doppler spectra from the received radar signals.

- `sophy_proc.py`: Main processing script that generates Plan Position Indicator
  (PPI) products. The script estimates radar moments including reflectivity,
  radial velocity, spectral width, and polarimetric variables, based on the
  **Pulse Pair** processing algorithm.
