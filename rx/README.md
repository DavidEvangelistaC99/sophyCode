## Reception Script

This folder contains the data acquisition script used for receiving radar
signals from a USRP device during the SOPHy experiments. The main script is **adapted from the `thor.py` receiver** provided in the
MIT Haystack **DigitalRF** repository. It has been customized to support
the SOPHy radar setup and data collection requirements. Received data are stored in **HDF5 format**, enabling efficient storage and
subsequent signal processing.

It include:

- `thor.py`: USRP-based receiver script for radar data acquisition and storage
  in HDF5 files.
