
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

class SignalProcessor:
    """Base class for signal processing operations."""
    def __init__(self, signal):
        self.signal = signal

    def compute_fft(self):
        # Compute FFT and frequency bins
        return np.fft.fft(self.signal), np.fft.fftfreq(len(self.signal))


class ExampleSignalProvider:
    """Provides example signals for quick testing."""
    @staticmethod
    def get_examples():
        return {
            'Sine': '0,0.71,1,0.71,0,-0.71,-1,-0.71',
            'Step': '1,1,1,1,0,0,0,0',
            'Impulse': '0,0,1,0,0,0,0,0',
            'Noise': ','.join(['{:.2f}'.format(x) for x in np.random.normal(0,1,8)])
        }


class MathExplanationProvider:
    """Provides math explanations for the UI."""
    @staticmethod
    def fft_explanation():
        return (
            "<b>FFT (Fast Fourier Transform)</b> decomposes a signal into its frequency components. "
            "The real part shows cosine (even) components, the imaginary part shows sine (odd) components. "
            "The magnitude spectrum shows the strength of each frequency in the signal."
        )


class InputValidator:
    """Validates user input for signal processing."""
    @staticmethod
    def validate_signal(signal):
        if len(signal) == 0:
            raise ValueError('Input signal is empty.')
        if not np.issubdtype(signal.dtype, np.floating) and not np.issubdtype(signal.dtype, np.integer):
            raise ValueError('Signal must be numeric.')

class SignalPlotter:
    """Handles plotting of signals and their transforms."""
    @staticmethod
    def plot_signal(signal, title='Input Signal'):
        fig, ax = plt.subplots()
        ax.plot(signal)
        ax.set_title(title)
        return fig

    @staticmethod
    def plot_fft(freq, fft, title='FFT Magnitude Spectrum', log_scale=False):
        """
        Plot the FFT magnitude spectrum. If log_scale is True, plot log10(magnitude + 1e-12).
        """
        fig, ax = plt.subplots()
        magnitude = np.abs(fft)
        if log_scale:
            magnitude = np.log10(magnitude + 1e-12)
            ax.set_ylabel('Log Magnitude')
        else:
            ax.set_ylabel('Magnitude')
        ax.stem(freq, magnitude)
        ax.set_title(title)
        return fig

class ImageEncoder:
    """Encodes matplotlib figures to base64 for web display."""
    @staticmethod
    def fig_to_base64(fig):
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close(fig)
        return img_base64

def signal_from_string(input_signal):
    # Convert to numpy array
    return np.array([float(x.strip()) for x in input_signal.split(',') if x.strip() != ''])
