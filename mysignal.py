from scipy.fftpack import fft,ifft
from scipy.io.wavfile import read,write
from scipy.signal import get_window
import numpy as np
#import Signal
#from pdb import set_trace

class Signal:

    def __init__(self, filename):#初始化
        self.rate, self.data = read(filename)
        self.dtype = self.data.dtype

    def write(self,filename):#写
        write(filename,self.rate,self.data)

    def amplify(self,gain):#放大，振幅乘系数
        gain = max(1.0,gain)
        self.data = np.array(self.data,dtype=np.float64)*gain
        self.data = np.array(self.data,dtype=self.dtype)

    def attenuate(self,gain):#衰减
        gain = max(0.0,gain)
        gain = min(1.0,gain)
        self.data = np.array(self.data,dtype=np.float64)*gain
        self.data = np.array(self.data,dtype=self.dtype)
        
    def changenansheng(self):
        #x=self.data
        fs=self.rate
        #x3=x*2
        FS=int(fs//1.3)
        self.rate=FS
        #self.data = np.array(x,dtype=self.dtype)

    def changetongsheng(self):
        #x=self.data
        fs=self.rate
        #x3=x*2
        FS=int(fs//0.8)
        self.rate=FS
        #self.data = np.array(x3,dtype=self.dtype)

    def banddenoise(self):#带通滤波器
        x=self.data
        b1,a1 = Signal.butter(4,10,'low')
        sf = Signal.filtfilt(b1,a1,x)
        b2,a2 = Signal.butter(4,2000,'high')
        x = Signal.filtfilt(b2,a2,sf)
        self.data = np.array(x,dtype=self.dtype)

    def moving_average_filter(self, N=5):#移动滤波器，设置阈值
        x = self.data
        N = max(2,N)
        N = min(len(x),N)
        y = []
        cum = sum(x[0:N])
        for i in range(len(x)):#遍历原参数
            y.append(cum/float(N))
            cum -= x[i]
            cum += x[(i+N)%len(x)]
        self.data = np.array(y,x.dtype)

    def noise_removal(self,noise):#去除噪声
        fft_size = 256
        hann_win = get_window('hann', fft_size)
        band_width = 16
        triang_bank = get_window('triang',band_width)
        freq_step = band_width//2
        freq_supp_size = fft_size//2+1

        num_bands = (freq_supp_size-band_width-1)//freq_step+1

        num_bands += 2

        # Get threshold for each frequency band
        noise_spectrum = fft(noise.data, fft_size)[0:freq_supp_size]
        zeros = np.zeros(freq_step, dtype=np.complex)
        noise_spectrum = np.hstack((zeros,noise_spectrum,zeros))

        thresholds = []
        for i in range(num_bands):
            start = i*freq_step
            band = noise_spectrum[start:start+band_width]*triang_bank
            energy = sum(map(lambda x:np.power(np.abs(x),2),band))
            thresholds.append(energy)

        # Pad the original signal to its end
        time_step = fft_size//2
        pad_size = time_step-len(self.data)%time_step+1
        num_frames = (len(self.data)-fft_size+pad_size)//time_step+1
        zeros = np.zeros(pad_size,self.dtype)
        data = np.hstack((self.data,zeros))

        # Pad 2 sides of the original signal with zeros
        zeros = np.zeros(time_step,self.dtype)
        data = np.hstack((zeros,data,zeros))
        num_frames += 2

        # Frame signal
        frames = []
        for i in range(num_frames):
            start = i*time_step
            frame = data[start:start+fft_size]*hann_win
            frames.append(frame)

        # Spectral analysis
        sharpness = 0.01
        new_frames = []
        for frame in frames:
            spectrum = fft(frame)[0:freq_supp_size]
            zeros = np.zeros(freq_step,dtype=np.complex)
            spectrum = np.hstack((zeros,spectrum,zeros))

            bands = []
            for i in range(num_bands):
                start = i*freq_step
                band = spectrum[start:start+band_width]*triang_bank
                energy = sum(map(lambda x:np.power(np.abs(x),2),band))
                diff = energy-thresholds[i]
                gain = 1.0/(1+np.exp(-sharpness*diff))#####
                band *= gain    # Attenuate
                bands.append(band)

            # Retrieve attenuated spectrum
            new_spectrum = np.zeros(freq_supp_size,dtype=np.complex)
            for i in range(freq_supp_size-1):
                band_1 = bands[i//freq_step]
                band_2 = bands[i//freq_step+1]
                new_spectrum[i] = band_1[freq_step+i%freq_step]+band_2[i%freq_step]
            new_spectrum[-1] = bands[-1][freq_step]
            # Construct input for inverse Fourier transform
            new_spectrum = np.hstack((new_spectrum,np.conj(new_spectrum[::-1][1:freq_supp_size-1])))
            # Retrieve attenuated frame
            new_frame = np.real(ifft(new_spectrum))
            new_frames.append(new_frame)

        # Retrieve attenuated signal
        new_data = np.zeros(len(self.data))
        for i in range(len(self.data)-1):
            frame_1 = new_frames[i//time_step]
            frame_2 = new_frames[i//time_step+1]
            new_data[i] = frame_1[time_step+i%time_step]+frame_2[i%time_step]
        new_data[-1] = new_frames[-1][time_step]
        self.data = np.array(new_data,dtype=self.dtype)

    def truncate_silence(self,threshold):#静音剪切
        fft_size = 256
        hann_win = get_window('hann',fft_size)
        # Pad the original signal to its end
        time_step = fft_size//2
        pad_size = time_step-len(self.data)%time_step+1
        num_frames = (len(self.data)-fft_size+pad_size)//time_step+1
        zeros = np.zeros(pad_size,self.dtype)
        data = np.hstack((self.data,zeros))

        # Pad 2 sides of the original signal with zeros
        zeros = np.zeros(time_step,self.dtype)
        data = np.hstack((zeros,data,zeros))
        num_frames += 2

        # Frame signal
        frames = []
        for i in range(num_frames):
            start = i*time_step
            frame = data[start:start+fft_size]*hann_win
            frames.append(frame)

        # Truncate silence
        new_frames = []
        for frame in frames:
            energy = sum(map(lambda x:np.power(np.abs(x),2),frame))
            if energy>threshold:
                new_frames.append(frame)

        # Retrieve truncated signal by adding up frames
        new_data = np.zeros((len(new_frames)-1)*time_step+1)
        for i in range(len(new_data)-1):
            frame_1 = new_frames[i//time_step]
            frame_2 = new_frames[i//time_step+1]
            new_data[i] = frame_1[time_step+i%time_step]+frame_2[i%time_step]
        new_data[-1] = new_frames[-1][time_step]
        self.data = np.array(new_data,dtype=self.dtype)
