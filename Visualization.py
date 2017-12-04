# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 11:42:21 2017

@author: Lenovo
"""

import pyaudio  
import pylab as pl  
import numpy as np 
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter

ymajorLocator = MultipleLocator(1000)
ymajorFormatter = FormatStrFormatter('%1.1f')

while(1):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 0.1
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    #print("Begin recording")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("End recording")
    
    stream.stop_stream()
    stream.close()
    #p.terminate()
    wave_data = np.fromstring(b''.join(frames), dtype=np.short)
    
    # 绘制波形准备工作：左右声道分离
    wave_data.shape = -1, 2  
    wave_data = wave_data.T
    time = np.arange(0, len(wave_data[0])) * (1.0 / RATE)
    
    #可视化
    #左声道设置
    ax1 = pl.subplot(211)
    ax1.yaxis.set_major_locator(ymajorLocator)
    ax1.yaxis.set_major_formatter(ymajorFormatter)
    ax1.yaxis.grid(True, which='major')
    pl.ylim(ymin = -5000, ymax = 5000)
    ax1.plot(time, wave_data[0])
    #右声道设置
    ax2 = pl.subplot(212)
    ax2.yaxis.set_major_locator(ymajorLocator)
    ax2.yaxis.set_major_formatter(ymajorFormatter)
    ax2.yaxis.grid(True, which='major')
    pl.ylim(ymin = -5000, ymax = 5000)
    ax2.plot(time, wave_data[1])
    #现实上0.1秒录入声音的波形
    pl.xlabel("time (seconds)")  
    pl.show()

p.get_device_count()
