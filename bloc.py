import numpy as np
import matplotlib.pyplot as plt
import digital_rf as drf
from gnuradio import blocks
from gnuradio import gr
from modFreq import chirpStandard, chirpCentral, chirpMod, chirpUsrp

amp = 1
IPP = 0.0004
DC = 15
samp_rate = 20000000
f_central = 0
bw = 4000000

'''
ipp_ = json_object['IPP']
dc_ = json_object['DC']
sr_ = json_object['sr']
fc_ = json_object['fc']
bw_ = json_object['bw']
amp_ = json_object['amp']
'''

chirp_param = 'chirp_amp_' + str(amp) + '_ipp_' + str(IPP) + '_dc_' + str(DC) + '_sr_' + str(samp_rate) + '_fc_' + str(f_central) + '_bw_' + str(bw)
chirp_file = '/home/idi/anaconda3/envs/sophy3.10/code/bin/' + chirp_param + '.bin'
numSamples = len(chirpUsrp(amp,IPP,DC,samp_rate,f_central,bw))

# Crear el flujo principal
tb = gr.top_block()

_1 = blocks.vector_source_c(chirpUsrp(amp,IPP,DC,samp_rate,f_central,bw), False, numSamples, [])
_2 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, numSamples)
_3 = blocks.skiphead(gr.sizeof_gr_complex*1, 0)
_4 = blocks.head(gr.sizeof_gr_complex*1, numSamples)
# Generación y ubicación del archivo
_5 = blocks.file_sink(gr.sizeof_gr_complex*1, chirp_file, False)
# blocks_file_sink_1.set_unbuffered(False)
# self.blocks_file_sink_1.set_unbuffered(False)

# Conectar los bloques
tb.connect(_1, _2, _3, _4, _5)

# Ejecutar el flujo
tb.start()
tb.wait()

'''

#z = np.zeros(8)
#a = [1,2,3,4,5,6,7,8]
#print(z)

#plt.plot(a,z)
#plt.show()

def read_txt(filename):
    code   = []
    lineas = [line.rstrip('\n') for line in open(filename)]
    print("####")
    print(lineas)
    for i in range(len(lineas)):
        tmp =[int(x) for x in lineas[i]]
        code.append(tmp)
    nCode  = len(lineas)
    nBaud  = len(lineas[0])

    print(code)
    print(nCode)
    print(nBaud)

    return code,nCode,nBaud

def cod2usrp(codigo):
    code_flip=[]
    for i in range(len(codigo)):
      if codigo[i]==1:
         code_flip.append(1)
      else:
        code_flip.append(-1)
    return code_flip

code, nCode, nBaud = read_txt("/home/idi/anaconda3/envs/sophy3.10/code/codeB/file_code/A-COMPLEMENTARY_CODE_2.txt")

print("HOLAAAA")
print(code)
inv = cod2usrp(codigo=code[0])
print(inv)

def rep_seq(x, rep=10):
    L = len(x) * rep
    res = np.zeros(L, dtype=x.dtype)
    idx = np.arange(len(x)) * rep
    for i in np.arange(rep):
        res[idx + i] = x
    return(res)

print(rep_seq(np.array(inv),10))

class example:
   def __init__(self):
      self.nombre = "Fido"
      self.edad = 23

yo = example()


print(yo.nombre,yo.edad)

'''

A = 1
ipp = 0.0004
dc = 15
sr = 20000000
fc = 2000000
b = 4000000
  
chirp = chirpUsrp(A, ipp, dc, sr, fc, b)
t = np.arange(len(chirp))

plt.plot(t, np.real(chirp))
plt.plot()
