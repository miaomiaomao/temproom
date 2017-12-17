from mysignal import Signal
from pydub import AudioSegment
import winsound
import wave
import os
global sounddegree
global noise_filter
global voicechange
sounddegree=50    #(-20~20）音量初始化为50
noise_filter=0   #最开始不滤波
voicechange=0   #最开始不变声
receive_video='yuanshi.wav'
x = Signal(receive_video)


#音量大小调节模块
sound = AudioSegment.from_wav(receive_video)
if  sounddegree>100:
    sounddegree=100
elif sounddegree<0:
    sounddegree=0
louder = sound + int((sounddegree-50)*0.4)
file_handle = louder.export("output.wav", format="wav")
receive_video="output.wav"
winsound.PlaySound(receive_video, winsound.SND_ALIAS)


#降噪模块
if noise_filter==1:
     x.banddenoise();
     x.write('output.wav')
     receive_video="output.wav"
elif noise_filter==2:
    noise = Signal('noise.wav')
    x.noise_removal(noise)
    x.write('denoise.wav')
    receive_video='denoise.wav'
winsound.PlaySound(receive_video, winsound.SND_ALIAS)

#变声模块
if voicechange==1:
     x.changenansheng();
     x.write('output.wav');
elif voicechange==2:
     x.changetongsheng();
     x.write('output.wav');

receive_video='denoise.wav'
winsound.PlaySound(receive_video, winsound.SND_ALIAS)
'''
noise = Signal('noise.wav')
x.noise_removal(noise)
x.write('denoise.wav')
receive_video='denoise.wav'
winsound.PlaySound(receive_video, winsound.SND_ALIAS)
'''