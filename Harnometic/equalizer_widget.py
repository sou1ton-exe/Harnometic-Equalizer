import os
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from datetime import datetime
import scipy.io.wavfile
import librosa
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import tempfile


class EqualizerWidget(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
        self.samples = None
        self.sampling_rate = None
        self.samples_after = None
        self.current_file = None
        self.temp_wav_file = None

        self.audio_player_before = QMediaPlayer()
        self.audio_player_after = QMediaPlayer()
        self.audio_player_before.setNotifyInterval(1)
        self.audio_player_after.setNotifyInterval(1)

        self.bands_powers = [0.0, 0.25, 0.50, 0.75, 1.0, 2.0, 3.0, 4.0, 5.0]
        
        self.band_slider = {}
        self.band_label = {}

        for index in range(10):
            slider_name = f'band_{index+1}'
            label_name = f'band_{index+1}_label'
            
            if hasattr(self, slider_name): self.band_slider[index] = getattr(self, slider_name)
            else: self.band_slider[index] = qtw.QSlider(qtc.Qt.Vertical)
                
            if hasattr(self, label_name): self.band_label[index] = getattr(self, label_name)
            else: self.band_label[index] = qtw.QLabel("1.0")
            
        for slider in self.band_slider.values(): slider.setDisabled(True)

        for index, slider in self.band_slider.items(): slider.sliderReleased.connect(lambda checked=False, index=index: self.slider_gain_updated(index))

        self.current_slider_gain = [1.0] * 10

        self.plot_widget = {
            'before': self.graph_before,
            'after': self.graph_after
        }

        self.spectrogram_widget = {
            'before': self.spectrogram_before,
            'after': self.spectrogram_after
        }

        self.data_line = {
            'before': None,
            'after': None
        }

    def setup_ui(self):
        main_layout = qtw.QVBoxLayout(self)
        
        load_layout = qtw.QHBoxLayout()
        self.file_label = qtw.QLabel("Файл не выбран")
        self.file_label.setObjectName("file_label")
        load_layout.addWidget(self.file_label)
        
        main_layout.addLayout(load_layout)

        graphs_layout = qtw.QHBoxLayout()
        
        left_widget = qtw.QWidget()
        left_layout = qtw.QVBoxLayout(left_widget)
        
        left_layout.addWidget(qtw.QLabel("🔊 Оригинальный сигнал"))
        self.graph_before = pg.PlotWidget()
        self.graph_before.setBackground('w')
        self.graph_before.showGrid(x=True, y=True)
        left_layout.addWidget(self.graph_before)
        
        self.spectrogram_before = pg.PlotWidget()
        self.spectrogram_before.setBackground('w')
        left_layout.addWidget(self.spectrogram_before)
        
        graphs_layout.addWidget(left_widget)

        right_widget = qtw.QWidget()
        right_layout = qtw.QVBoxLayout(right_widget)
        
        right_layout.addWidget(qtw.QLabel("🎚️ Обработанный сигнал"))
        self.graph_after = pg.PlotWidget()
        self.graph_after.setBackground('w')
        self.graph_after.showGrid(x=True, y=True)
        right_layout.addWidget(self.graph_after)
        
        self.spectrogram_after = pg.PlotWidget()
        self.spectrogram_after.setBackground('w')
        right_layout.addWidget(self.spectrogram_after)
        
        graphs_layout.addWidget(right_widget)
        
        main_layout.addLayout(graphs_layout)

        equalizer_layout = qtw.QVBoxLayout()
        equalizer_layout.addWidget(qtw.QLabel("🎛️ Регулировка частот"))
        
        bands_layout = qtw.QHBoxLayout()
        
        freq_ranges = [
            "20-60Hz", "60-120Hz", "120-250Hz", "250-500Hz", 
            "500-1kHz", "1-2kHz", "2-4kHz", "4-8kHz", "8-16kHz", "16-20kHz"
        ]
        
        for i in range(10):
            band_widget = qtw.QWidget()
            band_layout = qtw.QVBoxLayout(band_widget)
            
            freq_label = qtw.QLabel(freq_ranges[i])
            freq_label.setObjectName(f"band_{i+1}")
            freq_label.setAlignment(qtc.Qt.AlignCenter)
            freq_label.setStyleSheet("font-size: 10px;")
            band_layout.addWidget(freq_label)
            
            slider = qtw.QSlider(qtc.Qt.Vertical)
            slider.setRange(0, 8)
            slider.setValue(4)
            slider.setMinimumHeight(150)
            setattr(self, f'band_{i+1}', slider)
            band_layout.addWidget(slider)
            
            label = qtw.QLabel("1.0")
            label.setObjectName(f"band_{i+1}_label")
            label.setAlignment(qtc.Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold;")
            setattr(self, f'band_{i+1}_label', label)
            band_layout.addWidget(label)
            
            bands_layout.addWidget(band_widget)
        
        equalizer_layout.addLayout(bands_layout)
        
        self.reset_btn = qtw.QPushButton("🔄 Сбросить эквалайзер")
        self.reset_btn.clicked.connect(self.reset_equalizer)
        equalizer_layout.addWidget(self.reset_btn)
        
        self.save_file_btn = qtw.QPushButton("💾 Сохранить обработанный файл")
        self.save_file_btn.clicked.connect(self.save_processed_file)
        equalizer_layout.addWidget(self.save_file_btn)
        
        main_layout.addLayout(equalizer_layout)

    def load_audio_file(self, file_path):
        try:
            self.current_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            
            if self.temp_wav_file and os.path.exists(self.temp_wav_file):
                try: os.unlink(self.temp_wav_file)
                except: pass
            
            if file_path.lower().endswith('.mp3'):
                self.samples, self.sampling_rate = librosa.load(file_path, sr=None, mono=True)
                self.temp_wav_file = tempfile.mktemp(suffix='.wav')
                scipy.io.wavfile.write(self.temp_wav_file, self.sampling_rate, (self.samples * 32767).astype(np.int16))
                player_file_path = self.temp_wav_file
            else:
                self.sampling_rate, self.samples = scipy.io.wavfile.read(file_path)
                if len(self.samples.shape) > 1: self.samples = np.mean(self.samples, axis=1)
                player_file_path = file_path
            
            self.audio_player_before.setMedia(QMediaContent(qtc.QUrl.fromLocalFile(player_file_path)))
            
            for slider in self.band_slider.values(): slider.setDisabled(False)
            
            self.plot_graph(self.samples, self.sampling_rate, 'before')
            self.plot_spectrogram(self.samples, self.sampling_rate, 'before')
            
            self.modify_signal()
            
            return True
            
        except Exception as e:
            print(f"Ошибка загрузки файла: {e}")
            return False

    def plot_graph(self, samples, sampling_rate, widget):
        try:
            peak_value = np.max(np.abs(samples)) if len(samples) > 0 else 1.0
            normalized_data = samples / peak_value
            length = samples.shape[0] / sampling_rate
            time = np.linspace(0, length, samples.shape[0])

            self.plot_widget[widget].clear()
            drawing_pen = pg.mkPen(color=(255, 0, 0), width=1)
            
            self.data_line[widget] = self.plot_widget[widget].plot(time, normalized_data, pen=drawing_pen)
            self.plot_widget[widget].setLabel('left', 'Амплитуда')
            self.plot_widget[widget].setLabel('bottom', 'Время', 'с')
            self.plot_widget[widget].setXRange(0, np.max(time))
            self.plot_widget[widget].setYRange(-1.1, 1.1)
            
        except Exception as e: print(f"Ошибка построения графика: {e}")

    def plot_spectrogram(self, samples, sampling_rate, widget):
        try:
            self.spectrogram_widget[widget].clear()
            
            n_fft = 2048
            hop_length = 512
            
            stft = librosa.stft(samples, n_fft=n_fft, hop_length=hop_length)
            spectrogram = np.abs(stft)
            log_spectrogram = librosa.amplitude_to_db(spectrogram, ref=np.max)
            
            img = pg.ImageItem()
            self.spectrogram_widget[widget].addItem(img)
            
            img.setImage(log_spectrogram.T)
            
            self.spectrogram_widget[widget].setLabel('left', 'Частота', 'Hz')
            self.spectrogram_widget[widget].setLabel('bottom', 'Время', 'с')
            
            img.setRect(qtc.QRectF(0, 0, len(samples)/sampling_rate, sampling_rate/2))
            
        except Exception as e: print(f"Ошибка построения спектрограммы: {e}")

    def modify_signal(self):
        if self.samples is None: return

        try:
            frequency_content = np.fft.rfftfreq(len(self.samples), d=1/self.sampling_rate)
            modified_signal = np.fft.rfft(self.samples)
            
            for index, slider_gain in enumerate(self.current_slider_gain):
                frequency_range_min = (index + 0) * self.sampling_rate / (2 * 10)
                frequency_range_max = (index + 1) * self.sampling_rate / (2 * 10)

                range_min_frequency = frequency_content > frequency_range_min
                range_max_frequency = frequency_content <= frequency_range_max
                
                band_mask = range_min_frequency & range_max_frequency
                modified_signal[band_mask] *= slider_gain

            self.samples_after = np.fft.irfft(modified_signal)
            
            max_val = np.max(np.abs(self.samples_after))
            if max_val > 1.0: self.samples_after = self.samples_after / max_val

            self.save_output_wav()

            self.plot_graph(self.samples_after, self.sampling_rate, 'after')
            self.plot_spectrogram(self.samples_after, self.sampling_rate, 'after')
            
        except Exception as e: print(f"Ошибка обработки сигнала: {e}")

    def slider_gain_updated(self, index):
        try:
            slider_value = self.band_slider[index].value()
            if 0 <= slider_value < len(self.bands_powers):
                slider_gain = self.bands_powers[slider_value]
                self.band_label[index].setText(f'{slider_gain:.2f}')
                self.current_slider_gain[index] = slider_gain
                self.modify_signal()
                
        except Exception as e: print(f"Ошибка обновления слайдера: {e}")

    def save_output_wav(self):
        try:
            os.makedirs('wav', exist_ok=True)
            
            now = datetime.now()
            now_str = f'{now:%Y-%m-%d_%H-%M-%S}'
            output_path = f"wav/processed_{now_str}.wav"
            
            output_data = (self.samples_after * 32767).astype(np.int16)
            scipy.io.wavfile.write(output_path, self.sampling_rate, output_data)
            
            self.audio_player_after.setMedia(QMediaContent(qtc.QUrl.fromLocalFile(output_path)))
            
        except Exception as e: print(f"Ошибка сохранения файла: {e}")

    def save_processed_file(self):
        if self.samples_after is None:
            qtw.QMessageBox.warning(self, "Предупреждение", "Нет обработанного файла для сохранения")
            return
        
        try:
            original_name = os.path.basename(self.current_file) if self.current_file else "processed_audio"
            name, ext = os.path.splitext(original_name)
            
            file_path, _ = qtw.QFileDialog.getSaveFileName(
                self,
                "Сохранить обработанный файл",
                f"{name}_processed{ext}",
                "Аудио файлы (*.wav *.mp3);;WAV файлы (*.wav);;Все файлы (*)"
            )
            
            if file_path:
                output_data = (self.samples_after * 32767).astype(np.int16)
                scipy.io.wavfile.write(file_path, self.sampling_rate, output_data)
                
                qtw.QMessageBox.information(self, "Успех", f"Файл успешно сохранен:\n{file_path}")
                
        except Exception as e: qtw.QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def reset_equalizer(self):
        for i in range(10):
            self.band_slider[i].setValue(4)
            self.current_slider_gain[i] = 1.0
            self.band_label[i].setText("1.00")
        
        if self.samples is not None: self.modify_signal()