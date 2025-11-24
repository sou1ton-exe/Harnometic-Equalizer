from PyQt5.QtGui import QPalette, QColor, QFont


class DarkTheme:
    def __init__(self):
        self.primary_color = "#FF0000"
        self.accent_color = "#6A0000"
        self.background_dark = "#0F0F0F"
        self.background_medium = "#1A1A1A"
        self.background_light = "#252525"
        self.text_primary = "#FFFFFF"
        self.text_secondary = "#B3B3B3"
        self.text_muted = "#808080"
        self.hover_color = "#2A2A2A"
        self.selection_color = "#333333"
        self.success_color = "#A9A9A9"
        self.warning_color = "#FFA500"
        self.save_btn_color = "#00C507"
        
    def get_stylesheet(self):
        return f"""
            QMainWindow {{
                background-color: {self.background_dark};
                color: {self.text_primary};
            }}
            
            #sidebar {{
                background-color: {self.background_medium};
                border-right: 1px solid {self.background_light};
            }}
            
            #appHeader {{
                background-color: {self.primary_color};
                color: white;
                padding: 20px;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            #playlistFrame {{
                background-color: transparent;
            }}
            
            #playlistHeader {{
                color: {self.text_primary};
                font-size: 16px;
                font-weight: bold;
                padding: 10px 0px;
            }}
            
            #playlist {{
                background-color: transparent;
                border: 1px solid {self.background_light};
                border-radius: 8px;
                padding: 5px;
                font-size: 14px;
                outline: none;
                color: {self.text_primary};
            }}
            
            #playlist::item {{
                background-color: transparent;
                border-radius: 4px;
                padding: 8px 12px;
                margin: 2px 0px;
                color: {self.text_primary};
            }}
            
            #playlist::item:selected {{
                background-color: {self.selection_color};
                color: {self.text_primary};
            }}
            
            #playlist::item:hover {{
                background-color: {self.hover_color};
                color: {self.text_primary};
            }}
            
            #playlist::item:alternate {{
                background-color: {self.background_light};
                color: {self.text_primary};
            }}
            
            #mainArea {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.background_medium}, stop:1 {self.background_dark});
            }}
            
            #videoContainer {{
                background-color: #000000;
                border-bottom: 1px solid {self.background_light};
            }}
            
            #trackInfo {{
                color: {self.text_secondary};
                font-size: 16px;
                padding: 40px;
                font-weight: 500;
            }}
            
            #controlPanel {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.background_light}, stop:1 {self.background_medium});
                border-top: 1px solid {self.background_light};
            }}
            
            #primaryButton {{
                background-color: {self.primary_color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
                font-size: 12px;
            }}
            
            #primaryButton:hover {{
                background-color: #E60000;
            }}
            
            #primaryButton:pressed {{
                background-color: #CC0000;
            }}
            
            #secondaryButton {{
                background-color: {self.background_light};
                color: {self.text_primary};
                border: 1px solid {self.text_muted};
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
            }}
            
            #secondaryButton:hover {{
                background-color: {self.hover_color};
            }}
            
            #secondaryButton:pressed {{
                background-color: {self.selection_color};
            }}
            
            #controlButton {{
                background-color: {self.text_primary};
                border: 2px solid {self.text_muted};
                border-radius: 20px;
                padding: 0px;
                min-width: 50px;
                min-height: 50px;
            }}
            
            #controlButton:hover {{
                background-color: {self.hover_color};
                border-color: {self.text_secondary};
            }}
            
            #controlButton:pressed {{
                background-color: {self.selection_color};
            }}
            
            #playButton {{
                background-color: {self.primary_color};
                border: 2px solid {self.text_muted};
                border-radius: 20px;
                padding: 0px;
                min-width: 50px;
                min-height: 50px;
                margin: 0 10px;
            }}
            
            #playButton:hover {{
                background-color: #E60000;
                transform: scale(1.05);
            }}
            
            #playButton:pressed {{
                background-color: #CC0000;
            }}
            
            /* Ползунки */
            #positionSlider {{
                min-height: 20px;
            }}
            
            #positionSlider::groove:horizontal {{
                border: none;
                height: 6px;
                background: {self.background_light};
                border-radius: 3px;
                margin: 0px;
            }}
            
            #positionSlider::handle:horizontal {{
                background: {self.primary_color};
                border: 2px solid {self.text_primary};
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }}
            
            #positionSlider::handle:horizontal:hover {{
                background: #E60000;
                width: 18px;
                height: 18px;
                border-radius: 9px;
            }}
            
            #positionSlider::sub-page:horizontal {{
                background: {self.primary_color};
                border-radius: 3px;
            }}
            
            #volumeSlider {{
                min-height: 20px;
            }}
            
            #volumeSlider::groove:horizontal {{
                border: none;
                height: 4px;
                background: {self.background_light};
                border-radius: 2px;
                margin: 0px;
            }}
            
            #volumeSlider::handle:horizontal {{
                background: {self.text_primary};
                border: 2px solid {self.text_primary};
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }}
            
            #volumeSlider::handle:horizontal:hover {{
                background: {self.primary_color};
            }}
            
            #volumeSlider::sub-page:horizontal {{
                background: {self.text_primary};
                border-radius: 2px;
            }}
            
            #timeLabel {{
                color: {self.text_secondary};
                font-size: 12px;
                font-weight: 500;
                padding: 0 10px;
            }}
            
            #volumeLabel {{
                color: {self.text_secondary};
                font-size: 12px;
                font-weight: 500;
                min-width: 30px;
                padding-left: 5px;
            }}
            
            #statusBar {{
                background-color: {self.background_light};
                color: {self.text_secondary};
                border-top: 1px solid {self.background_light};
            }}
            
            QLabel[objectName="volumeIcon"] {{
                color: {self.text_secondary};
                font-size: 14px;
                padding-right: 5px;
            }}

            EqualizerWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.background_dark}, stop:1 {self.background_medium});
                border: 1px solid {self.background_light};
                border-radius: 12px;
                padding: 15px;
                color: {self.text_primary};
            }}
            
            EqualizerWidget QLabel {{
                color: {self.text_primary};
                background-color: transparent;
            }}
            
            #equalizerTitle {{
                color: {self.text_primary};
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.primary_color}, stop:1 {self.accent_color});
                border-radius: 8px;
                margin: 5px;
            }}
            
            QPushButton[text="💾 Сохранить обработанный файл"] {{
                background-color: {self.background_light};
                color: {self.text_primary};
                border: 2px solid {self.save_btn_color};
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 13px;
                font-weight: bold;
                margin: 10px 5px;
            }}
            
            QPushButton[text="💾 Сохранить обработанный файл"]:hover {{
                background-color: {self.save_btn_color};
                color: white;
            }}
            
            QPushButton[text="💾 Сохранить обработанный файл"]:pressed {{
                background-color: #00B106;
            }}
            
            QPushButton[text="🔄 Сбросить эквалайзер"] {{
                background-color: {self.background_light};
                color: {self.text_primary};
                border: 2px solid {self.primary_color};
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 13px;
                font-weight: bold;
                margin: 10px 5px;
            }}
            
            QPushButton[text="🔄 Сбросить эквалайзер"]:hover {{
                background-color: {self.primary_color};
                color: white;
            }}
            
            QPushButton[text="🔄 Сбросить эквалайзер"]:pressed {{
                background-color: #CC0000;
            }}        
            
            QSlider::groove:vertical {{
                background: {self.hover_color};
                border: 1px solid {self.text_muted};
                width: 8px;
                border-radius: 100px;
            }}
            
            QSlider::handle:vertical {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.hover_color}, stop:1 {self.background_light});
                border: 2px solid {self.text_muted};
                height: 20px;
                width: 20px;
                border-radius: 10px;
                margin: 0px -6px;
            }}
            
            QSlider::handle:vertical:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.hover_color}, stop:1 {self.text_primary});
                border: 2px solid {self.success_color};
            }}
            
            QSlider::handle:vertical:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.success_color}, stop:1 {self.hover_color});
            }}
            
            QLabel[objectName^="band_"] {{
                color: {self.text_primary};
                font-size: 10px;
                font-weight: bold;
                background-color: {self.background_light};
                border: 1px solid {self.text_muted};
                border-radius: 4px;
                padding: 2px 4px;
                margin: 2px;
            }}
            
            QLabel[objectName$="_label"] {{
                color: {self.text_primary} !important;
                font-size: 11px;
                font-weight: bold;
                background-color: {self.background_dark};
                border: 1px solid {self.primary_color};
                border-radius: 6px;
                padding: 4px 6px;
                min-width: 30px;
            }}
            
            PlotWidget {{
                background-color: {self.background_dark};
                border: 2px solid {self.background_light};
                border-radius: 8px;
                padding: 5px;
            }}
            
            QLabel[text="🔊 Оригинальный сигнал"],
            QLabel[text="🎚️ Обработанный сигнал"] {{
                color: {self.text_primary};
                font-size: 14px;
                font-weight: bold;
                background-color: {self.background_light};
                border-radius: 6px;
                padding: 8px 12px;
                margin: 5px;
            }}
            
            QPushButton[text="▶️ Воспр."],
            QPushButton[text="⏸️ Пауза"],
            QPushButton[text="⏹️ Стоп"] {{
                background-color: {self.background_light};
                color: {self.text_primary};
                border: 2px solid {self.text_muted};
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 11px;
                font-weight: bold;
                min-width: 70px;
            }}
            
            QPushButton[text="▶️ Воспр."]:hover,
            QPushButton[text="⏸️ Пауза"]:hover,
            QPushButton[text="⏹️ Стоп"]:hover {{
                background-color: {self.hover_color};
                border-color: {self.primary_color};
            }}
            
            QPushButton[text="▶️ Воспр."]:pressed,
            QPushButton[text="⏸️ Пауза"]:pressed,
            QPushButton[text="⏹️ Стоп"]:pressed {{
                background-color: {self.primary_color};
                color: white;
            }}
            
            QLabel[objectName="file_label"] {{
                color: {self.text_secondary};
                font-size: 12px;
                font-style: italic;
                background-color: {self.background_light};
                border: 1px solid {self.text_muted};
                border-radius: 4px;
                padding: 6px 10px;
                margin: 5px;
            }}
            
            QWidget[objectName*="graph"],
            QWidget[objectName*="spectrogram"] {{
                background-color: {self.background_dark};
                border: 1px solid {self.background_light};
                border-radius: 6px;
                margin: 2px;
            }}
            
            QSlider:disabled {{
                background-color: transparent;
            }}
            
            QSlider::groove:vertical:disabled {{
                background: {self.background_light};
                border: 1px solid {self.text_muted};
            }}
            
            QSlider::handle:vertical:disabled {{
                background: {self.text_muted};
                border: 2px solid {self.background_light};
            }}
        """
    
    def get_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(self.background_dark))
        palette.setColor(QPalette.WindowText, QColor(self.text_primary))
        palette.setColor(QPalette.Base, QColor(self.background_medium))
        palette.setColor(QPalette.AlternateBase, QColor(self.background_light))
        palette.setColor(QPalette.ToolTipBase, QColor(self.text_primary))
        palette.setColor(QPalette.ToolTipText, QColor(self.text_primary))
        palette.setColor(QPalette.Text, QColor(self.text_primary))
        palette.setColor(QPalette.Button, QColor(self.background_light))
        palette.setColor(QPalette.ButtonText, QColor(self.text_primary))
        palette.setColor(QPalette.BrightText, QColor(self.primary_color))
        palette.setColor(QPalette.Link, QColor(self.primary_color))
        palette.setColor(QPalette.Highlight, QColor(self.primary_color))
        palette.setColor(QPalette.HighlightedText, QColor(self.text_primary))
        
        return palette
    
    def get_font(self):
        font = QFont("Segoe UI", 9)
        return font