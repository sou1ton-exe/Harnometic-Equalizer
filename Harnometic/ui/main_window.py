from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QSlider, QLabel, QListWidget, QSplitter, 
                             QStyle, QStatusBar, QFrame)
from PyQt5.QtCore import Qt
from styles.themes import DarkTheme
from equalizer_widget import EqualizerWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Harnometic | by Sou1toon | v1.0.0")
        self.setGeometry(100, 100, 1400, 800)
        
        self.setup_ui()
        self.apply_theme()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        splitter = QSplitter(Qt.Horizontal)
        
        self.setup_sidebar(splitter)
        
        self.setup_main_area(splitter)
        
        splitter.setSizes([350, 1050])
        main_layout.addWidget(splitter)
        
        self.setup_control_panel(main_layout)
        
        self.setup_status_bar()
        
    def setup_sidebar(self, splitter):
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        app_header = QLabel("Harnometic")
        app_header.setObjectName("appHeader")
        app_header.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(app_header)
        
        self.setup_playlist_widget()
        sidebar_layout.addWidget(self.playlist_frame)
        
        splitter.addWidget(sidebar)
        
    def setup_playlist_widget(self):
        self.playlist_frame = QFrame()
        self.playlist_frame.setObjectName("playlistFrame")
        playlist_layout = QVBoxLayout(self.playlist_frame)
        playlist_layout.setContentsMargins(15, 15, 15, 15)
        playlist_layout.setSpacing(10)
        
        playlist_header = QLabel("Ваша музыка")
        playlist_header.setObjectName("playlistHeader")
        playlist_layout.addWidget(playlist_header)
        
        self.playlist_widget = QListWidget()
        self.playlist_widget.setObjectName("playlist")
        self.playlist_widget.setAlternatingRowColors(True)
        playlist_layout.addWidget(self.playlist_widget)
        
        self.setup_playlist_buttons(playlist_layout)
        
    def setup_playlist_buttons(self, layout):
        buttons_layout = QHBoxLayout()
        
        self.add_files_btn = QPushButton("Добавить треки")
        self.add_files_btn.setObjectName("primaryButton")
        
        self.remove_file_btn = QPushButton("Удалить")
        self.remove_file_btn.setObjectName("secondaryButton")
        
        self.clear_playlist_btn = QPushButton("Очистить")
        self.clear_playlist_btn.setObjectName("secondaryButton")
        
        buttons_layout.addWidget(self.add_files_btn)
        buttons_layout.addWidget(self.remove_file_btn)
        buttons_layout.addWidget(self.clear_playlist_btn)
        
        layout.addLayout(buttons_layout)
        
    def setup_main_area(self, splitter):
        main_area = QWidget()
        main_area.setObjectName("mainArea")
        main_layout = QVBoxLayout(main_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.equalizer_widget = EqualizerWidget()
        self.equalizer_widget.setObjectName("equalizerWidget")
        main_layout.addWidget(self.equalizer_widget)
        
        self.track_info = QLabel("")
        self.track_info.setObjectName("trackInfo")
        self.track_info.setAlignment(Qt.AlignCenter)
        self.track_info.setMinimumHeight(60)
        main_layout.addWidget(self.track_info)
        
        splitter.addWidget(main_area)
        
    def setup_control_panel(self, parent_layout):
        control_panel = QWidget()
        control_panel.setObjectName("controlPanel")
        control_panel.setFixedHeight(120)
        control_layout = QVBoxLayout(control_panel)
        control_layout.setContentsMargins(30, 15, 30, 15)
        control_layout.setSpacing(10)
        
        progress_layout = QHBoxLayout()
        
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setObjectName("positionSlider")
        progress_layout.addWidget(self.position_slider)
        
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setObjectName("timeLabel")
        self.time_label.setFixedWidth(120)
        progress_layout.addWidget(self.time_label)
        
        control_layout.addLayout(progress_layout)
        
        controls_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton()
        self.prev_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.prev_btn.setObjectName("controlButton")
        self.prev_btn.setToolTip("Предыдущий трек")
        
        self.play_btn = QPushButton()
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.setObjectName("playButton")
        self.play_btn.setToolTip("Воспроизведение/Пауза")
        
        self.stop_btn = QPushButton()
        self.stop_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_btn.setObjectName("controlButton")
        self.stop_btn.setToolTip("Стоп")
        
        self.next_btn = QPushButton()
        self.next_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.next_btn.setObjectName("controlButton")
        self.next_btn.setToolTip("Следующий трек")
        
        controls_layout.addStretch()
        controls_layout.addWidget(self.prev_btn)
        controls_layout.addWidget(self.play_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.next_btn)
        controls_layout.addStretch()
        
        volume_layout = QHBoxLayout()
        volume_layout.setSpacing(8)
        
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.setToolTip("Громкость")
        volume_layout.addWidget(self.volume_slider)
        
        self.volume_label = QLabel("50%")
        self.volume_label.setObjectName("volumeLabel")
        volume_layout.addWidget(self.volume_label)
        
        controls_layout.addLayout(volume_layout)
        
        control_layout.addLayout(controls_layout)
        parent_layout.addWidget(control_panel)
        
    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("statusBar")
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Готов к воспроизведению")
        
    def apply_theme(self):
        theme = DarkTheme()
        self.setStyleSheet(theme.get_stylesheet())
        
        palette = theme.get_palette()
        self.setPalette(palette)
        
        self.setFont(theme.get_font())