from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import logging

class SpectralPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        logging.info("SpectralPlotWidget initialized.")

    def plot_spectra(self, roi_data, roi_color='blue', plot_mean=True, plot_std=False):
        try:
            self.figure.clear()

            ax = self.figure.add_subplot(111)
            x = range(len(roi_data['spectra']))

            if plot_mean:
                mean = roi_data['mean']
                ax.plot(x, mean, label='Mean', color=roi_color)

            if plot_std:
                std = roi_data['std']
                ax.fill_between(x, mean-std, mean+std, color=roi_color, alpha=0.2, label='Standard Deviation')

            ax.legend()
            self.canvas.draw()
            logging.info("Spectra plotted successfully.")
        except Exception as e:
            logging.error("Error plotting spectra: %s", e, exc_info=True)