## Transmission Scripts

This folder contains the transmission-related scripts used in the SOPHy radar
experiments. These scripts are responsible for waveform generation and
transmission using a USRP platform.
The transmission workflow is **based on and adapted from the `tx.py` script**
of the MIT Haystack **DigitalRF** repository, with modifications to support
the SOPHy radar configuration and experimental requirements.

It includes:

- `modFreq.py`: Script for generating the chirp waveform used in the radar
  experiments. This script defines the modulation parameters and produces
  the frequency-modulated signal transmitted by the radar.

- `tx.py`: USRP-based transmission script that loads the generated waveform
  and handles the transmission configuration.
