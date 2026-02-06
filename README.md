# FFT Visualizer

A simple Flask web app to visualize the Fast Fourier Transform (FFT) of a user-input signal.

## Features
- Enter a list of numbers as a signal
- View the input signal plot
- View the FFT magnitude spectrum

## Setup
1. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On Mac/Linux
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
4. Open your browser and go to http://127.0.0.1:5000/

## Example Input
```
1, 0, -1, 0, 1, 0, -1, 0
```

## Next Steps
- Add more math visualizations (SVD, eigen decomposition, algorithm complexity)
- Improve UI/UX
- Add input validation and error handling
