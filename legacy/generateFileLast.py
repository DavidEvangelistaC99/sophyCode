## -- Este programa crea el archivo .json y .bin -- ##

import json
import argparse

###---Define Chirp Signal Parameters---###

parser = argparse.ArgumentParser(description = '###---Parameters Chirp Signal---###')

parser.add_argument('-amp','--amplitude',dest='amplitude',type=float,default=1,help='''Amplitude in -. (default: 1)''')
parser.add_argument('-IPP','--ipp_seg',dest='ipp_seg',type=float,default=0.0004,help='''IPP in seg. (default: waveform default or 400e-6 - 60km)''')
parser.add_argument('-DC','--dc',dest='dc',type=float,default=15,help='''DC in percentage. (default: 15 percent)''')
parser.add_argument('-sr_tx','--samp_rate_tx',dest='samp_rate_tx',type=float,default=20000000,help='''Sample rate TX in Hz. (default: 20 MHz)''')
parser.add_argument('-sr_rx','--samp_rate_rx',dest='samp_rate_rx',type=float,default=10000000,help='''Sample rate RX in Hz. (default: 10 MHz)''')
parser.add_argument('-fc','--central_freq',dest='central_freq',type=float,default=1000000,help='''Central Frequency in Hz. (default: 1 MHz)''')
parser.add_argument('-bw','--band_width',dest='band_width',type=float,default=1000000,help='''Band Width in Hz. (default: 1 MHz)''')
parser.add_argument('-t','--t_delay',dest='t_delay',type=float,default=0,help='''Delay Time in ms. (default: 0 us)''')
parser.add_argument('-w','--window',dest='window',type=str,default='r',help='''Chirp Window. (default: 'r')''')
parser.add_argument('-dirJ','--json_dir',dest='json_dir',type=str,default=None,help='''Directory Location of JSON''')
parser.add_argument('-nrep','--nRep',dest='nRep',type=float,default=None,help='''Chirp Repetitions''')

args = parser.parse_args()

file_dir_json = args.json_dir

###---Writing JSON file---###

###---Parameters---###

data = {'IPP': args.ipp_seg, 'dc_1': args.dc, 'sr_tx': args.samp_rate_tx, 'sr_rx': args.samp_rate_rx, 'fc_1': args.central_freq, 'bw_1': args.band_width, 'window_1': args.window, 'time_d_1': args.t_delay, 'amplitude_1': args.amplitude, 'repetitions_1': args.nRep}
# name = 'chirp_ipp_'+str(data['IPP'])+'_dc_'+str(data['DC'])+'_srTx_'+str(data['sr_tx'])+'_srRx_'+str(data['sr_rx'])+'_fc_'+str(data['fc'])+'_bw_'+str(data['bw'])+'_amp_'+str(data['amp'])+'.json'
name = 'chirp_1.json'
dirJ = str(file_dir_json)
dirJ = dirJ + '/' + name

with open(dirJ, 'w') as f:	# Load to file
    json.dump(data, f)

###---Opening JSON file---###

with open(dirJ,'r') as openfile:
 
    # Reading from json file
    json_object = json.load(openfile)

print(json_object)


######################################################################
########################### OJO IMPORTANTE ###########################
######################################################################

# Comandos anteriores
# python3 generateFileLast.py -IPP 0.0004 -DC 15 -sr_tx 20000000 -sr_rx 5000000 -fc 0 -bw 2000000 -amp 1 -dirJ /home/idi/anaconda3/envs/sophy3.10/code/json -dirB /home/idi/anaconda3/envs/sophy3.10/code/bin
# python3 generateFileLast.py -IPP 0.0004 -DC 15 -sr_tx 20000000 -sr_rx 5000000 -fc -1000000 -bw 2200000 -amp 1 -dirJ /home/idi/anaconda3/envs/sophy3.10/code/json -dirB /home/idi/anaconda3/envs/sophy3.10/code/bin
# python3 generateFileLast.py -amp 1 -IPP 0.0004 -DC 15 -sr_tx 20000000 -sr_rx 5000000 -fc 0 -bw 2200000 -dirJ /home/idi/anaconda3/envs/sophy3.10/code/json
# python3 generateFileLast.py -amp 1 -IPP 0.0004 -DC 15 -sr_tx 20000000 -sr_rx 5000000 -fc 0 -bw 4000000 -dirJ /home/idi/anaconda3/envs/sophy3.10/code/json
# python3 generateFileLast.py -amp 0.5 -IPP 0.0004 -DC 5 -sr_tx 20000000 -sr_rx 5000000 -fc 0 -bw 4000000 -t 0 -w r -dirJ /home/idi/anaconda3/envs/sophy3.10/code/json

# Versión para el ejemplo del uso de SIRM
# python3 generateFileLast.py -amp 0.5 -IPP 400.0e-6 -DC 2.0 -sr_tx 20.0e6 -sr_rx 5.0e6 -fc 0.0 -bw 4.0e6 -t 0 -w B -dirJ /home/idi/anaconda3/envs/sophy3.10/code/json
# python3 generateFileLast.py -amp 0.5 -IPP 400.0e-6 -DC 2.0 -sr_tx 20.0e6 -sr_rx 5.0e6 -fc 0.0 -bw 4.0e6 -t 0 -w B -nrep 500 -dirJ /home/idi/anaconda3/envs/sophy3.10/code/json
# python3 generateFileLast.py -amp 1.0 -IPP 400.0e-6 -DC 1.0 -sr_tx 20.0e6 -sr_rx 2.5e6 -fc 2.0e6 -bw 0.0e6 -t 5.2 -w R -nrep 5 -dirJ /home/idi/anaconda3/envs/sophy3.10/code/json
