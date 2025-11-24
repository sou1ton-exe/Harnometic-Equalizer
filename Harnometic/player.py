from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QStyle, QFileDialog, QPushButton, QWidget, QHBoxLayout
from ui.main_window import MainWindow
import os


class MediaPlayer(MainWindow):
    def __init__(self):
        super().__init__()
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.playlist = []
        self.current_index = 0
        self.current_file = None
        self.play_processed_audio = False
        self.setup_toggle_button()
        self.setup_media_connections()
        
    def setup_toggle_button(self):
        self.toggle_audio_btn = QPushButton("🎚️ Оригинал")
        self.toggle_audio_btn.setObjectName("secondaryButton")
        self.toggle_audio_btn.setToolTip("Переключить между оригинальным и обработанным звуком")
        self.toggle_audio_btn.setCheckable(True)
        self.toggle_audio_btn.setChecked(False)
        
        control_panel = self.findChild(QWidget, "controlPanel")
        if control_panel:
            controls_layout = control_panel.findChild(QHBoxLayout)
            if controls_layout: controls_layout.insertWidget(5, self.toggle_audio_btn)  # Подберите нужный индекс
        
    def setup_media_connections(self):
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.stateChanged.connect(self.state_changed)
        self.equalizer_widget.audio_player_before.positionChanged.connect(self.position_changed)
        self.equalizer_widget.audio_player_before.durationChanged.connect(self.duration_changed)
        self.equalizer_widget.audio_player_before.stateChanged.connect(self.state_changed)
        self.equalizer_widget.audio_player_after.positionChanged.connect(self.position_changed)
        self.equalizer_widget.audio_player_after.durationChanged.connect(self.duration_changed)
        self.equalizer_widget.audio_player_after.stateChanged.connect(self.state_changed)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.play_btn.clicked.connect(self.play_pause)
        self.stop_btn.clicked.connect(self.stop)
        self.prev_btn.clicked.connect(self.previous)
        self.next_btn.clicked.connect(self.next)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.position_slider.sliderPressed.connect(self.slider_pressed)
        self.position_slider.sliderReleased.connect(self.slider_released)
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected_item)
        self.add_files_btn.clicked.connect(self.add_files)
        self.remove_file_btn.clicked.connect(self.remove_file)
        self.clear_playlist_btn.clicked.connect(self.clear_playlist)
        
        if hasattr(self, 'toggle_audio_btn'): self.toggle_audio_btn.toggled.connect(self.on_audio_mode_toggled)

        self.is_slider_dragging = False

    def on_audio_mode_toggled(self, checked):
        self.play_processed_audio = checked
        
        if checked:
            self.toggle_audio_btn.setText("🎛️ Обработанный")
            self.status_bar.showMessage("Режим: обработанный звук (эквалайзер применен)")
        else:
            self.toggle_audio_btn.setText("🎚️ Оригинал")
            self.status_bar.showMessage("Режим: оригинальный звук")
            
        if self.is_playing(): self.switch_audio_player()

    def get_current_player(self):
        if self.play_processed_audio: return self.equalizer_widget.audio_player_after
        else: return self.media_player

    def is_playing(self):
        return (self.media_player.state() == QMediaPlayer.PlayingState or
                self.equalizer_widget.audio_player_before.state() == QMediaPlayer.PlayingState or
                self.equalizer_widget.audio_player_after.state() == QMediaPlayer.PlayingState)

    def stop_all_players(self):
        self.media_player.stop()
        self.equalizer_widget.audio_player_before.stop()
        self.equalizer_widget.audio_player_after.stop()

    def pause_all_players(self):
        self.media_player.pause()
        self.equalizer_widget.audio_player_before.pause()
        self.equalizer_widget.audio_player_after.pause()

    def switch_audio_player(self):
        if self.is_playing():
            current_position = self.get_current_player().position()

            self.pause_all_players()

            if self.play_processed_audio:
                self.equalizer_widget.audio_player_after.setPosition(current_position)
                self.equalizer_widget.audio_player_after.play()
            else:
                self.media_player.setPosition(current_position)
                self.media_player.play()

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Выберите аудиофайлы", "", 
                                               "Аудиофайлы (*.wav *.mp3 *.flac *.m4a *.aac *.ogg)")
        if files:
            for file in files:
                self.playlist.append(file)
                filename = os.path.basename(file)
                self.playlist_widget.addItem(filename)
            
            if len(self.playlist) == len(files): self.play_file(0)
                
            self.status_bar.showMessage(f"✅ Добавлено {len(files)} треков", 3000)

    def remove_file(self):
        current_row = self.playlist_widget.currentRow()
        if current_row >= 0:
            removed_item = self.playlist_widget.takeItem(current_row)
            self.playlist.pop(current_row)
            
            if current_row == self.current_index:
                if self.playlist:
                    if current_row >= len(self.playlist):
                        self.current_index = len(self.playlist) - 1
                        self.play_file(self.current_index)
                    else: self.play_file(self.current_index)
                else:
                    self.stop_all_players()
                    self.current_index = 0
                    
            self.status_bar.showMessage(f"🗑️ Удален трек: {removed_item.text()}", 3000)

    def clear_playlist(self):
        self.playlist_widget.clear()
        self.playlist.clear()
        self.stop_all_players()
        self.current_index = 0
        self.status_bar.showMessage("🧹 Плейлист очищен", 3000)

    def play_selected_item(self, item):
        row = self.playlist_widget.row(item)
        self.play_file(row)

    def play_file(self, index):
        if 0 <= index < len(self.playlist):
            self.current_index = index
            self.current_file = self.playlist[index]
        
            try:
                self.stop_all_players()
                
                media_content = QMediaContent(QUrl.fromLocalFile(self.current_file))
                self.media_player.setMedia(media_content)
            
                success = self.equalizer_widget.load_audio_file(self.current_file)
            
                if success:
                    if self.play_processed_audio: self.equalizer_widget.audio_player_after.play()
                    else: self.media_player.play()
                
                    track_name = os.path.basename(self.current_file)
                    self.track_info.setText("")
                    mode_text = " (обработанный)" if self.play_processed_audio else " (оригинальный)"
                    self.status_bar.showMessage(f"▶️ Воспроизведение: {track_name}{mode_text}")
                
                    self.playlist_widget.setCurrentRow(index)
                    
                    self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
                    
                else: self.status_bar.showMessage("❌ Не удалось загрузить в эквалайзер", 5000)
                
            except Exception as e: self.status_bar.showMessage(f"❌ Ошибка загрузки файла: {str(e)}", 5000)

    def play_pause(self):
        if not self.current_file and self.playlist:
            self.play_file(self.current_index)
            return
            
        if not self.current_file:
            self.status_bar.showMessage("📭 Плейлист пуст", 3000)
            return

        current_player = self.get_current_player()
        
        if current_player.state() == QMediaPlayer.PlayingState:
            current_player.pause()
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.status_bar.showMessage("⏸️ Пауза", 2000)
        else:
            current_player.play()
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            mode_text = " (обработанный)" if self.play_processed_audio else " (оригинальный)"
            self.status_bar.showMessage(f"▶️ Воспроизведение{mode_text}", 2000)

    def stop(self):
        self.stop_all_players()
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.track_info.setText("Выберите трек для воспроизведения")
        self.status_bar.showMessage("⏹️ Остановлено", 2000)

    def previous(self):
        if self.playlist:
            self.current_index = (self.current_index - 1) % len(self.playlist)
            self.play_file(self.current_index)

    def next(self):
        if self.playlist:
            self.current_index = (self.current_index + 1) % len(self.playlist)
            self.play_file(self.current_index)

    def set_volume(self, value):
        self.media_player.setVolume(value)
        self.equalizer_widget.audio_player_before.setVolume(value)
        self.equalizer_widget.audio_player_after.setVolume(value)
        self.volume_label.setText(f"{value}%")

    def set_position(self, position):
        if self.is_slider_dragging:
            current_player = self.get_current_player()
            current_player.setPosition(position)

    def position_changed(self, position):
        if not self.is_slider_dragging: self.position_slider.setValue(position)
        self.update_time()

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def state_changed(self, state):
        sender = self.sender()
        current_player = self.get_current_player()
        
        if sender == current_player:
            if state == QMediaPlayer.PlayingState: self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            else: self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def update_time(self):
        current_player = self.get_current_player()
        current_time = current_player.position() // 1000
        total_time = current_player.duration() // 1000
        
        if total_time > 0:
            current_min = current_time // 60
            current_sec = current_time % 60
            total_min = total_time // 60
            total_sec = total_time % 60
            
            self.time_label.setText(f"{current_min:02d}:{current_sec:02d} / {total_min:02d}:{total_sec:02d}")

    def slider_pressed(self): self.is_slider_dragging = True

    def slider_released(self):
        self.is_slider_dragging = False
        position = self.position_slider.value()
        current_player = self.get_current_player()
        current_player.setPosition(position)