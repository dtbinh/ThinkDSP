def generate_bpsk_signal(bits, rate=8000, symbol_len = 250, freq = 1000):
    """
    Returns a numpy array which is a BPSK encoding of bits
    1 symbol worth of zeros are added at the beginning and the end to aid detection of transmission start
    A 1 bit is added to the beginning to help with synchronization

    s_n(t) =   \sqrt{\frac{2E_b}{T_b}} \cos(2 \pi f_c t + \pi(1-n )), n = 0,1. 

    Arguments
    ---------
    bits -  a numpy array of 1s and 0s
    rate - sample rate used
    symbol_len - length in samples of the rectangular pulse used to encode the bits
    freq - carrier frequency in Hz
    """
    # extend with symbol len
    bits = np.concatenate([np.tile(bit, symbol_len) for bit in bits])
    
    # A 1 bit is added to the beginning to help with synchronization
    bits = np.concatenate((np.ones(symbol_len), bits))
    
    # Convert 0 and 1's to -1 and 1 
    bits = 2 * (bits - 0.5)
    
    # m(t) * cos(wt)
    foo = []
    ts = np.arange(0, len(bits)/float(rate), 1/float(rate))
    for t, n in zip(ts, bits):
        foo += [7000*n * np.cos(2 * np.pi * freq * t)]    
    
    return np.concatenate((np.zeros(symbol_len), foo, np.zeros(symbol_len)))
    

def decode_bpsk_signal(x, freq=1000, rate = 8000, symbol_len = 250, detection_threshold_factor = 0.3, LPFbw = 320):
    """
    Decodes a received BPSK signal in vector x and produces a numpyarray of bits 
    The function uses a brute-force approach to carrier phase synchronization by checking 16 evenly spaced
    phase offsets between -pi and pi to find the one which results in the strongest demodulated signal
    which is then used as the demodulated signal
    The first bit is assumed to be a control bit that always equals 1. This bit is not returned in the final output
    
    Arguments
    ---------
    x - a numpy array of the received audio samples
    freq - carrier frequency 
    rate - sample rate used 
    symbol_len - length in samples of the rectangular pulse
    detection_threshold_factor - this is used for detecting the start and end of transmission
                              the start of transmission is the first sample that exceeds
                              detection_threshold_factor times the maximum value in x
                              the end of transmission is the last sample that exceeds
                              detection_threshold_factor times the maximum value in x
    LPFbw - this is the bandwidth in rad/sec of the low-pass filter that is used after
         multiplying with a cosine
    """
    pass