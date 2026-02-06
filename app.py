import numpy as np
from flask import Flask, render_template, request, send_file, jsonify
import csv
from io import TextIOWrapper
import os

from signal_processing import (
    SignalProcessor, SignalPlotter, ImageEncoder, signal_from_string,
    ExampleSignalProvider, MathExplanationProvider, InputValidator
)
from fibonacci import FibonacciCalculator


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/fft', methods=['GET', 'POST'])
def fft_visualizer():
    plot_url = None
    freq_url = None
    real_url = None
    imag_url = None
    input_signal = ''
    error = None
    math_explanation = MathExplanationProvider.fft_explanation()
    example_signals = ExampleSignalProvider.get_examples()
    if request.method == 'POST':
        input_signal = request.form.get('signal', '')
        file = request.files.get('csvfile')
        # FFT visualization options
        subtract_mean = 'subtract_mean' in request.form
        normalize_fft = 'normalize_fft' in request.form
        log_scale = 'log_scale' in request.form
        try:
            if file and file.filename:
                # Read CSV file, expect a single row or column of numbers
                wrapper = TextIOWrapper(file, encoding='utf-8')
                reader = csv.reader(wrapper)
                values = []
                for row in reader:
                    for val in row:
                        try:
                            values.append(float(val.strip()))
                        except Exception:
                            continue
                signal = np.array(values)
                input_signal = ','.join(str(x) for x in signal)
            else:
                signal = signal_from_string(input_signal)
            InputValidator.validate_signal(signal)

            # Optionally subtract mean
            if subtract_mean:
                signal = signal - np.mean(signal)

            processor = SignalProcessor(signal)

            # Plot input signal
            fig_signal = SignalPlotter.plot_signal(processor.signal)
            plot_url = ImageEncoder.fig_to_base64(fig_signal)

            # Compute FFT
            fft, freq = processor.compute_fft()
            # Optionally normalize
            if normalize_fft:
                fft = fft / len(fft)

            # Plot FFT magnitude spectrum (optionally log scale)
            fig_fft = SignalPlotter.plot_fft(freq, fft, log_scale=log_scale)
            freq_url = ImageEncoder.fig_to_base64(fig_fft)

            # Plot real and imaginary parts
            fig_real = SignalPlotter.plot_signal(np.real(fft), title='FFT Real Part')
            real_url = ImageEncoder.fig_to_base64(fig_real)
            fig_imag = SignalPlotter.plot_signal(np.imag(fft), title='FFT Imaginary Part')
            imag_url = ImageEncoder.fig_to_base64(fig_imag)
        except Exception as e:
            error = f"Error: {str(e)}"
            plot_url = None
            freq_url = None
            real_url = None
            imag_url = None

    return render_template(
        'index.html',
        plot_url=plot_url,
        freq_url=freq_url,
        real_url=real_url,
        imag_url=imag_url,
        input_signal=input_signal,
        error=error,
        math_explanation=math_explanation,
        example_signals=example_signals
    )


# Fibonacci calculator route
@app.route('/fibonacci', methods=['GET', 'POST'])
def fibonacci():
    result = None
    error = None
    n = ''
    mode = 'single'
    download_ready = False
    if request.method == 'POST':
        n = request.form.get('n', '')
        mode = request.form.get('mode', 'single')
        try:
            n_int = int(n)
            if n_int < 0:
                raise ValueError('n must be non-negative')
            fib_calc = FibonacciCalculator()
            if mode == 'single':
                result = fib_calc.number(n_int)
            else:
                result = fib_calc.sequence(n_int)
                download_ready = True
        except Exception as e:
            error = f"Error: {str(e)}"
    return render_template('fibonacci.html', result=result, error=error, n=n, mode=mode, download_ready=download_ready)

# Route to download Fibonacci sequence as CSV
import io
@app.route('/download_fibonacci_csv')
def download_fibonacci_csv():
    n = int(request.args.get('n', '0'))
    fib_calc = FibonacciCalculator()
    seq = fib_calc.sequence(n)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Index', 'Fibonacci'])
    for idx, val in enumerate(seq):
        writer.writerow([idx, val])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'fibonacci_sequence_n{n}.csv'
    )








if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
