#!python
# ----------------------------------------------------------------------------
# Copyright (c) 2017 Massachusetts Institute of Technology (MIT)
# All rights reserved.
#
# Distributed under the terms of the BSD 3-clause license.
#
# The full license is in the LICENSE file, distributed with this software.
# ----------------------------------------------------------------------------
"""Create pseudorandom-coded waveform files for sounding.

See the following paper for a description and application of meteor radar using
pseudorandom codes:

Vierinen, J., Chau, J. L., Pfeffer, N., Clahsen, M., and Stober, G.,
Coded continuous wave meteor radar, Atmos. Meas. Tech., 9, 829-839,
doi:10.5194/amt-9-829-2016, 2016.

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import math
from argparse import ArgumentParser

import numpy
import scipy.signal
# rate 1 Mhz
# ipp = 60 Km---> 400 puntos
def create_code_test(clen = 400, dutycicle=50):
    z   = numpy.zeros(clen)
    o   = 1*numpy.ones(clen)#524288 ojo 1
    cod = numpy.zeros([clen])
    N   = z.shape[0]
    print("muestras",(dutycicle/100.0)*clen)

    for ri in numpy.arange(N):
        if ri< (dutycicle/100.0)*clen:
            cod[ri]=o[ri]
        else:
            #cod[ri]=o[ri]/2.0
            cod[ri]=0#o[ri]/2.0

    '''
    cod[0]= 1

    cod[1]=-1
    cod[2]= 1
    cod[3]= 0
    cod[4]= 0
    cod[5]= 1
    cod[6]= 1
    cod[7]=-1
    '''
    '''
    cod[0]= 1
    cod[1]= 1
    cod[2]= 1
    #cod[3]= 1
    '''
    '''
    cod[1]= 0
    cod[2]= 0
    cod[3]= 0
    cod[4]= -1
    cod[5]= -1
    cod[6]= -1
    cod[7]= -1
    cod[8]= 0
    cod[9]= 0
    cod[10]= 0
    cod[11]= 0
    cod[12]= 1
    cod[13]= 1
    cod[14]= 1
    cod[15]= 1
    '''
    cod= numpy.roll(cod,290)

    # estaba en 110  aprox 5.8 useg
    # estaba en 220  aprox 10 useg
    # estaba en 230  aprox


    print(cod[280:310])
    #phases=numpy.array(numpy.exp(1.0j*2.0*math.pi*cod),dtype= numpy.complex64)
    #print(phases.shape)
    #print (phases)
    return (cod)

def wr_waveform_to_file(ipp_km=60,dutycicle=50,sample_rate=1):
    #longitud del codigo
    clen = int((ipp_km*sample_rate*10**3)/150.0)#150 denominador
    print("clen",clen)
    a= create_code_test(clen=clen,dutycicle=dutycicle)

    name='code-test-%dkm-DC-%.5f-r-%1.2fMhz-wrv0.bin'% (ipp_km, dutycicle,sample_rate)
    print(name)
    a.tofile(name)



# seed is a way of reproducing the random code without
# having to store all actual codes. the seed can then
# act as a sort of station_id.
def create_pseudo_random_code(clen=10000, seed=0):
    numpy.random.seed(seed)
    phases = numpy.array(
        numpy.exp(1.0j * 2.0 * math.pi * numpy.random.random(clen)),
        dtype=numpy.complex64,
    )
    return(phases)


# oversample a phase code by a factor of rep
def rep_seq(x, rep=10):
    L = len(x) * rep
    res = numpy.zeros(L, dtype=x.dtype)
    idx = numpy.arange(len(x)) * rep
    for i in numpy.arange(rep):
        res[idx + i] = x
    return(res)


#
# lets use 0.1 s code cycle and coherence assumption
# our transmit bandwidth is 100 kHz, and with a 10e3 baud code,
# that is 0.1 seconds per cycle as a coherence assumption.
# furthermore, we use a 1 MHz bandwidth, so we oversample by a factor of 10.
#
def waveform_to_file(
    station=0, clen=10000, oversample=10, filter_output=False,
):
    a = rep_seq(
        create_pseudo_random_code(clen=clen, seed=station),
        rep=oversample,
    )
    if filter_output:
        w = numpy.zeros([oversample * clen], dtype=numpy.complex64)
        fl = (int(oversample + (0.1 * oversample)))
        w[0:fl] = scipy.signal.blackmanharris(fl)
        aa = numpy.fft.ifft(numpy.fft.fft(w) * numpy.fft.fft(a))
        a = aa / numpy.max(numpy.abs(aa))
        a = numpy.array(a, dtype=numpy.complex64)
        a.tofile('code-l%d-b%d-%06df.bin' % (clen, oversample, station))
    else:
        a.tofile('code-l%d-b%d-%06d.bin' % (clen, oversample, station))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-ipp', '--ipp_km', type=int, default=60,
        help='''Code length (IPP Km). (default: %(default)s)''',
    )
    parser.add_argument(
        '-r', '--sample_rate', type=float, default=1,
        help='''Sample rate in Mhz (Tx). (default: %(default)s)''',
    )
    parser.add_argument(
        '-b', '--oversampling', type=int, default=10,
        help='''Oversampling factor (number of samples per baud).
                (default: %(default)s)''',
    )
    parser.add_argument(
        '-s', '--station', type=int, default=0,
        help='''Station ID (seed). (default: %(default)s)''',
    )
    parser.add_argument(
        '-f', '--filter', action='store_true',
        help='''Filter waveform with Blackman-Harris window.
                (default: %(default)s)''',
    )

    parser.add_argument(
        '-d', '--dutycicle', type=float, default=4,
        help='''Dutycicle ( Percentage of the number of ones per code).
                (default: %(default)s)''',
    )


    op = parser.parse_args()

    #waveform_to_file(
    #    station=op.station, clen=op.length, oversample=op.oversampling,
    #    filter_output=op.filter,
    #)

    wr_waveform_to_file(ipp_km=op.ipp_km,dutycicle=op.dutycicle,sample_rate=op.sample_rate)
