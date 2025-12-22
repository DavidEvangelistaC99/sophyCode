# ahora si con ntx

import numpy as np

def read_txt(filename):
    code   = []
    lineas = [line.rstrip('\n') for line in open(filename)] # ['11', '10']
    for i in range(len(lineas)):
        tmp =[int(x) for x in lineas[i]]
        code.append(tmp)
    
    #code -> [[1, 1], [1, 0]]
    nCode  = len(lineas)    # Numero de filas: 2
    nBaud  = len(lineas[0]) # Numero de columnas o bits de cada fila: 2
    return code,nCode,nBaud

# Conversion de bits: 1s a 1s y 0s a -1s
# codigo -> lista de bits: 1 o 0
def cod2usrp(codigo):
    code_flip=[]
    for i in range(len(codigo)):
      if codigo[i]==1:
         code_flip.append(1)
      else:
        code_flip.append(-1)
    return code_flip

# Devuelve la rep repeticion de cada uno de los elementos de un arreglo 
# x -> arreglo de numeros
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
        # code = np.fromfile(file_code_A,dtype= np.complex64)
        # code -> lista de las filas de codigos del archivos .txt
        # nCode -> Numero de filas de cada .txt
        code,nCode,nBaud = read_txt(file_code_A)
        print("Imprimimos code...")
        print(code)
        print("nCode")
        print(nCode)
        if nCode<2:
          print("Hola")
          code_arr= np.array(code,dtype=np.complex64)
          # Al parecer deberia ser code_arr[0] para poder analizar y cambiar los bits, porque esta tomando el arreglo no sus bits internos
          tmp_code = cod2usrp(codigo=code_arr)

          # Numero de puntos del duty cycle A
          dc_ = DCA*samp_rate
          # Numero de puntos para cada codigo dentro del duty cycle
          num = dc_/len(code_arr)
          rep =int(round(num))
          # Aca tambien puede afectar la misma observacion de code_arr[0]
          out_code  = rep_seq(np.array(tmp_code,dtype=np.float64),rep)
          CODEA = np.hstack((out_code, np.zeros(int(round((IPP-DCA)*samp_rate)))))
    if file_code_A is None or nCode<2: 
      print("Paso")
      for i in range(int(NTXA)):
          if i==0:
              CODE_TA= CODEA
          else:
              CODE_TA= np.hstack((CODE_TA,CODEA))
    else:
      print("HOLAAAAA")

      iter_cod = 0
      for i in range(int(NTXA)) :
          code_arr = np.array(code[iter_cod],dtype=np.complex64)
          print(code_arr)
          tmp_code = cod2usrp(codigo=code_arr)
          print(tmp_code)
          rep =int(round(DCA*samp_rate/len(code_arr)))
          out_code  = rep_seq(np.array(tmp_code,dtype=np.float64),rep)
          print(out_code)
          CODEA = np.hstack((out_code, np.zeros(int(round((IPP-DCA)*samp_rate)))))
          print(CODEA)
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
              out_code  = rep_seq(np.array(tmp_code,dtype=np.float64),rep)
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
              out_code  = rep_seq(np.array(tmp_code,dtype=np.float64),rep)
              CODEB = np.hstack((out_code, np.zeros(int(round((IPP-DCB)*samp_rate)))))
              iter_cod=iter_cod+1
              if iter_cod == nCode:
                  iter_cod =0
              if i==0:
                  CODE_TB=CODEB
              else:
                  CODE_TB= np.hstack((CODE_TB,CODEB))


    # Variables finales: TOTAL
    if NTXB== 0:
        TOTAL = CODE_TA
    else:
        # Si hay NTXB se manda la union de los dos
        TOTAL = np.hstack((CODE_TA,CODE_TB))
    clendelay =int(delay*samp_rate)
    print(len(TOTAL),clendelay,delay)
    TOTAL_ROLL = np.roll(TOTAL,clendelay)
    return  TOTAL_ROLL
