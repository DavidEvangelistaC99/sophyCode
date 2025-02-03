## -- Este programa crea el archivo .json y .bin -- ##

import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
import digital_rf as drf
from gnuradio import blocks
from gnuradio import gr
from modFreq import chirpStandard, chirpCentral, chirpMod, chirpUsrp

###---Define Chirp Signal Parameters---###

parser = argparse.ArgumentParser(description = '###---Parameters Chirp Signal---###')

parser.add_argument('-IPP','--ipp_seg',dest='ipp_seg',type=float,default=0.0004,help='''IPP in seg. (default: waveform default or 400e-6 - 60km)''')
parser.add_argument('-DC','--dc',dest='dc',type=float,default=15,help='''DC in percentage. (default: 15 percent)''')
parser.add_argument('-sr','--samp_rate',dest='samp_rate',type=float,default=20000000,help='''Sample rate in Hz. (default: 20 MHz)''')
parser.add_argument('-fc','--central_freq',dest='central_freq',type=float,default=1000000,help='''Central Frequency in Hz. (default: 1 MHz)''')
parser.add_argument('-bw','--band_width',dest='band_width',type=float,default=1000000,help='''Band Width in Hz. (default: 1 MHz)''')
parser.add_argument('-amp','--amplitude',dest='amplitude',type=float,default=1,help='''Amplitude in -. (default: 1)''')
parser.add_argument('-dirJ','--json_dir',dest='json_dir',type=str,default=None,help='''Directory Location of JSON''')
parser.add_argument('-dirB','--bin_dir',dest='bin_dir',type=str,default=None,help='''Directory Location OF BIN''')

args = parser.parse_args()

file_dir_json = args.json_dir
file_dir_bin = args.bin_dir

###---Writing JSON file---###

###---Parameters---###

data = {'IPP': args.ipp_seg, 'DC': args.dc, 'sr': args.samp_rate, 'fc': args.central_freq, 'bw': args.band_width, 'amp': args.amplitude}
name = 'chirp_ipp_'+str(data['IPP'])+'_dc_'+str(data['DC'])+'_sr_'+str(data['sr'])+'_fc_'+str(data['fc'])+'_bw_'+str(data['bw'])+'_amp_'+str(data['amp'])+'.json'
dirJ = str(file_dir_json)
dirJ = dirJ + '/' + name

with open(dirJ, 'w') as f:	#Load to file
    json.dump(data, f)

###---Opening JSON file---###

with open(dirJ,'r') as openfile:
 
    # Reading from json file
    json_object = json.load(openfile)

print(json_object)

###---Creación de archivo .bin---###

# Definición de parámetros
ipp_ = json_object['IPP']
dc_ = json_object['DC']
sr_ = json_object['sr']
fc_ = json_object['fc']
bw_ = json_object['bw']
amp_ = json_object['amp']

chirp_param = 'chirp_amp_' + str(amp_) + '_ipp_' + str(ipp_) + '_dc_' + str(dc_) + '_sr_' + str(sr_) + '_fc_' + str(fc_) + '_bw_' + str(bw_)
dirB = str(file_dir_bin)
chirp_file = str(dirB + '/' + chirp_param + '.bin')

numSamples = len(chirpUsrp(amp_, ipp_, dc_, sr_, fc_, bw_))

# Crear el flujo principal
tb = gr.top_block()

_1 = blocks.vector_source_c(chirpUsrp(amp_, ipp_, dc_, sr_, fc_, bw_), False, numSamples, [])
_2 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, numSamples)
_3 = blocks.skiphead(gr.sizeof_gr_complex*1, 0)
_4 = blocks.head(gr.sizeof_gr_complex*1, numSamples)

# Generación y ubicación del archivo
_5 = blocks.file_sink(gr.sizeof_gr_complex*1, chirp_file, False)

# Conectar los bloques
tb.connect(_1, _2, _3, _4, _5)

# Ejecutar el flujo
tb.start()
tb.wait()

# Usado ahora
# python3 generateFile.py -IPP 0.0004 -DC 15 -sr 20000000 -fc 2000000 -bw 4000000 -amp 1 -dirJ /home/idi/anaconda3/envs/sophy3.10/code/json -dirB /home/idi/anaconda3/envs/sophy3.10/code/bin
