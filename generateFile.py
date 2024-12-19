import json
import argparse

###---Define Chirp Signal Parameters---###

parser = argparse.ArgumentParser(description ='###---Parameters Chirp Signal---###')

parser.add_argument('-IPP','--ipp_seg',dest='ipp_seg',type=float,default=0.0004,help='''IPP in seg. (default: waveform default or 400e-6 - 60km)''')
parser.add_argument('-DC','--dc',dest='dc',type=float,default=15,help='''DC in percentage. (default: 15 percent)''')
parser.add_argument('-sr','--samp_rate',dest='samp_rate',type=float,default=20000000,help='''Sample rate in Hz. (default: 20 MHz)''')
parser.add_argument('-fc','--central_freq',dest='central_freq',type=float,default=1000000,help='''Central Frequency in Hz. (default: 1 MHz)''')
parser.add_argument('-bw','--band_width',dest='band_width',type=float,default=1000000,help='''Band Width in Hz. (default: 1 MHz)''')
parser.add_argument('-amp','--amplitude',dest='amplitude',type=float,default=1,help='''Amplitude in -. (default: 1)''')

args = parser.parse_args()

###---Writing JSON file---###

##--Parameters--##

data = {'IPP': args.ipp_seg, 'DC': args.dc, 'sr': args.samp_rate, 'fc': args.central_freq, 'bw': args.band_width, 'amp': args.amplitude}
name = 'chirp_ipp_'+str(data['IPP'])+'_dc_'+str(data['DC'])+'_sr_'+str(data['sr'])+'_fc_'+str(data['fc'])+'_bw_'+str(data['bw'])+'_amp_'+str(data['amp'])

with open(name+'.json', 'w') as f:	#Load to file
    json.dump(data, f)

###---Opening JSON file---###

with open(name + '.json','r') as openfile:
 
    # Reading from json file
    json_object = json.load(openfile)

print(name+'.json')
print(json_object)
print(type(json_object))


###---Example---###
#python3 generateFile.py -IPP 0.0004 -DC 15 -sr 20000000 -fc 0 -bw 4000000 -amp 1 
