# ahora si con ntx

import numpy as np

def read_txt(filename):
    code   = []
    lineas = [line.rstrip('\n') for line in open(filename)]
    for i in range(len(lineas)):
        tmp =[int(x) for x in lineas[i]]
        code.append(tmp)
    nCode  = len(lineas)
    nBaud  = len(lineas[0])
    return code,nCode,nBaud


def cod2usrp(codigo):
    code_flip=[]
    for i in range(len(codigo)):
      if codigo[i]==1:
         code_flip.append(1)
      else:
        code_flip.append(-1)
    return code_flip


def rep_seq(x, rep=10):
    L = len(x) * rep
    res = np.zeros(L, dtype=x.dtype)
    idx = np.arange(len(x)) * rep
    for i in np.arange(rep):
        res[idx + i] = x
    return(res)

def newExperiment(IPP,NTXA,NTXB,DCA,DCB,file_code_A,file_code_B,samp_rate,delay):
    if file_code_A == None:
        val1 = (DCA*samp_rate) 
        val2 = (IPP-DCA)*samp_rate
        #round necesario porque generaba problemas los decimales
        CODEA = np.hstack((np.ones(int(round(val1))), np.zeros(int(round(val2)))))
        nCode = 0
    else:
        #code = np.fromfile(file_code_A,dtype= np.complex64)
        code,nCode,nBaud = read_txt(file_code_A)
        if nCode<2:
          code_arr= np.array(code,dtype=np.complex64)
          tmp_code = cod2usrp(codigo=code_arr)
          rep =int(round(DCA*samp_rate/len(code_arr)))
          out_code  = rep_seq(np.array(tmp_code,dtype=np.float_),rep)
          CODEA = np.hstack((out_code, np.zeros(int(round((IPP-DCA)*samp_rate)))))
    if file_code_A is None or nCode<2: 
      for i in range(int(NTXA)):
          if i==0:
              CODE_TA= CODEA
          else:
              CODE_TA= np.hstack((CODE_TA,CODEA))
    else:
      iter_cod = 0
      for i in range(int(NTXA)) :
          code_arr = np.array(code[iter_cod],dtype=np.complex64)
          tmp_code = cod2usrp(codigo=code_arr)
          rep =int(round(DCA*samp_rate/len(code_arr)))
          out_code  = rep_seq(np.array(tmp_code,dtype=np.float_),rep)
          CODEA = np.hstack((out_code, np.zeros(int(round((IPP-DCA)*samp_rate)))))
          iter_cod=iter_cod+1
          if iter_cod == nCode:
             iter_cod =0
          if i==0:
              CODE_TA=CODEA
          else:
              CODE_TA= np.hstack((CODE_TA,CODEA))  

    if  NTXB == 0:
        pass
    else:
        if file_code_B == None:
            val1=DCB*samp_rate
            val2=(IPP-DCB)*samp_rate
            CODEB = np.hstack((np.ones(int(round(val1))), np.zeros(int(round(val2)))))
            nCode=0
        else:
            code,nCode,nBaud = read_txt(file_code_B)
            #code = np.fromfile(file_code_B,dtype= np.complex64)
            if nCode <2:
              code_arr= np.array(code,dtype=np.complex64)
              tmp_code = cod2usrp(codigo=code_arr)
              rep =int(round(DCB*samp_rate/len(code)))
              out_code  = rep_seq(np.array(tmp_code,dtype=np.float_),rep)
              CODEB = np.hstack((out_code, np.zeros(int(round((IPP-DCB)*samp_rate)))))
        if file_code_B is None or nCode<2:
          for j in range(int(NTXB)):
              if j==0:
                  CODE_TB= CODEB
              else:
                  CODE_TB= np.hstack((CODE_TB,CODEB))
        else:
          iter_cod = 0
          for i in range(int(NTXB)) :
              code_arr = np.array(code[iter_cod],dtype=np.complex64)
              tmp_code = cod2usrp(codigo=code_arr)
              rep =int(round(DCB*samp_rate/len(code_arr)))
              out_code  = rep_seq(np.array(tmp_code,dtype=np.float_),rep)
              CODEB = np.hstack((out_code, np.zeros(int(round((IPP-DCB)*samp_rate)))))
              iter_cod=iter_cod+1
              if iter_cod == nCode:
                  iter_cod =0
              if i==0:
                  CODE_TB=CODEB
              else:
                  CODE_TB= np.hstack((CODE_TB,CODEB))

    if NTXB== 0:
        TOTAL = CODE_TA
    else:
        TOTAL = np.hstack((CODE_TA,CODE_TB))
    clendelay =int(delay*samp_rate)
    print(len(TOTAL),clendelay,delay)
    TOTAL_ROLL = np.roll(TOTAL,clendelay)
    return  TOTAL_ROLL
