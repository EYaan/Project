```

import time, zpop 
from pop import PiezoBuzzer
from datetime import datetime
import paho.mqtt.client as mqtt
import BlynkLib

blynk = BlynkLib.Blynk('LVJ4lNh64WzmrrbkTP3UTstk_upaqwdh', server="127.0.0.1", port=8080)
pb = PiezoBuzzer()
check_time = ""
check_emgtime = []
 
@blynk.VIRTUAL_WRITE(8)  
def sw8(n):
    if n[0]=='1' or n[0]=='0':
        pb.setTempo(120)
        pb.tone(4, 10, 4)

@blynk.VIRTUAL_WRITE(7)
def sw7(n):
    if n[0]=='1' or n[0]=='0':
        f = open("/home/soda/Documents/{}.txt".format(zpop.time_values[zpop.count-1]), "w")
        for i in range(len(zpop.time_values)-2):
            f.write("Temp = {}, Humi = {}, Cds = {}, Psd = {}, Time = {}\n".format(zpop.temp_values[i],zpop.humi_values[i],zpop.cds_values[i],zpop.psd_values[i],zpop.time_values[i]))
        f.close()

@blynk.VIRTUAL_WRITE(5)
def sw5(n):
    if n[0]=='1' or n[0]=='0':
        
        @blynk.VIRTUAL_READ(0)
        def start():
            global check_time
            blynk.virtual_write(0, zpop.temp_values[zpop.count - 1])
            blynk.virtual_write(1, zpop.humi_values[zpop.count - 1])
            blynk.virtual_write(2, zpop.cds_values[zpop.count - 1])
            blynk.virtual_write(3, zpop.psd_values[zpop.count - 1])
            
            if zpop.count > 5 and eve.emergency():
                if check_time == "" or check_time != ''.join(zpop.strange_v):
                    #check_emgtime.append(zpop.time_values[zpop.count - 1]) 
                    blynk.virtual_write(4, "add", zpop.emg_count, zpop.time_values[zpop.count - 1], ''.join(zpop.strange_v))
                    check_time = ''.join(zpop.strange_v)

@blynk.VIRTUAL_WRITE(6)
def sw6(n):
    
    if n[0]=='1' or n[0]=='0':
        blynk.virtual_write(4, "clr")

if __name__ == "__main__":

    
    zsw = zpop.zSWitches()      
    zds = zpop.zCds()
    zps = zpop.zPsd()
    zsh = zpop.zSht20()
    eve = zpop.values_everage()

    while True:
       
        zpop.count += 1

        zpop.time_values.append(datetime.now())
        zds.read_cds()
        zps.read_psd()
        zsh.read_sht20()
        zsw.read_Switch1()
        eve.read_everage()
            
        blynk.run()

from datetime import datetime
import paho.mqtt.client as mqtt
from pop import Oled, Switches, Psd, Cds, Sht20


count = 0  

emg_count = 0

emg = {}


cds_values = []
psd_values = []
temp_values = []
humi_values = []
time_values = []
v_everage = {}

strange_v = []

# emgv_temp = []
# emgv_humi = []
# emgv_psd = []
# emgv_cds = []
# emgv_time = []

tott = 0
toth = 0
totc = 0
totp = 0

def caller(func):
    def wrapper(*args, **kwargs):

        global count
        global cds_values
        global psd_values
        global temp_values
        global humi_values
        global time_values

        if func.__name__ == "read_cds":
            cds_values.append(func(*args, **kwargs))
        if func.__name__ == "read_psd":
            psd_values.append(func(*args, **kwargs))
        if func.__name__ == "read_sht20":
            temp_values.append(func(*args, **kwargs)[0])
            humi_values.append(func(*args, **kwargs)[1])
        ret = func(*args, **kwargs)
        return ret

    return wrapper

def disp():
    return print(
        "==={}번째 측정===\ncds : {}\npsd : {}\ntemp : {}\nhumi : {}\ntime : {}".format(count, cds_values[count - 1]
                                                                                    , psd_values[count - 1],
                                                                                    temp_values[count - 1],
                                                                                    humi_values[count - 1],
                                                                                    time_values[count - 1]))

class zSWitches(Switches):

    @caller
    def read_Switch0(self):
        return not Switches()[0].read()

    @caller
    def read_Switch1(self):
        return not Switches()[1].read()

class zCds(Cds):

    @caller
    def read_cds(self):
        return round(Cds().readAverage(), 2)

class zPsd(Psd):

    @caller
    def read_psd(self):
        return round(Psd().calcDist(Psd().readAverage()), 2)

class zSht20(Sht20):

    @caller
    def read_sht20(self):
        return round(Sht20().readTemp(), 2), round(Sht20().readHumi(), 2)

class values_everage:

    def read_everage(self):
        global count, cds_values, psd_values, temp_values, humi_values, time_values, v_everage, tott, toth, totc, totp

        tott += temp_values[count - 1]
        toth += humi_values[count - 1]
        totc += cds_values[count - 1]
        totp += psd_values[count - 1]

        v_everage['temp_values'] = round((tott / count), 2)
        v_everage['humi_values'] = round((toth / count), 2)
        v_everage['cds_values'] = round((totc / count), 2)
        v_everage['psd_values'] = round((totp / count), 2)

    def emergency(self):

        global v_everage
        global emg
        global emg_count
        global strange_v

        emg = {}
        strange_v = []


        if v_everage['temp_values'] < float(temp_values[count - 1]) - 15:
            emg['temp_values_high'] = True
            strange_v.append('T')
            
            
        elif v_everage['temp_values'] > float(temp_values[count - 1]) + 15:
            emg['temp_values_low'] = True
            strange_v.append('T')
            

        if v_everage['humi_values'] < float(humi_values[count - 1]) - 15:
            emg['humi_values_high'] = True
            strange_v.append('H')
            
        elif v_everage['humi_values'] > float(humi_values[count - 1]) + 15:
            emg['humi_values_low'] = True
            strange_v.append('H')
            

        if v_everage['cds_values'] < float(cds_values[count - 1]) - 200:
            emg['cds_values_high'] = True
            strange_v.append('C')
            
        elif v_everage['cds_values'] > float(cds_values[count - 1]) + 200:
            emg['cds_values_low'] = True
            strange_v.append('C')
            

        if v_everage['psd_values'] < float(psd_values[count - 1]) - 50:
            emg['psd_values_high'] = True
            strange_v.append('P')
            
        elif v_everage['psd_values'] > float(psd_values[count - 1]) + 50:
            emg['psd_values_low'] = True
            strange_v.append('P')
            

        for i in emg.values():
            if i == True:
                emg_count += 1

                return True

        return False
```
