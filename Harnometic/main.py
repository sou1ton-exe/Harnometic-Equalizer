"    @Telegram Channel: https://t.me/s_lowcode_w                                                          "
"    @Author's support: https://dalink.to/sou1toon                                                        "
"    |----------------------------------------- by sou1toon -----------------------------------------|    "
"    |                                                                                               |    "
"    |        ██╗░░██╗░█████╗░██████╗░███╗░░██╗░█████╗░███╗░░░███╗███████╗████████╗██╗░█████╗░       |    "
"    |        ██║░░██║██╔══██╗██╔══██╗████╗░██║██╔══██╗████╗░████║██╔════╝╚══██╔══╝██║██╔══██╗       |    "
"    |        ███████║███████║██████╔╝██╔██╗██║██║░░██║██╔████╔██║█████╗░░░░░██║░░░██║██║░░╚═╝       |    "
"    |        ██╔══██║██╔══██║██╔══██╗██║╚████║██║░░██║██║╚██╔╝██║██╔══╝░░░░░██║░░░██║██║░░██╗       |    "
"    |        ██║░░██║██║░░██║██║░░██║██║░╚███║╚█████╔╝██║░╚═╝░██║███████╗░░░██║░░░██║╚█████╔╝       |    "
"    |        ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚════╝░╚═╝░░░░░╚═╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░       |    "
"    |                                                                                               |    "
"    |------------------------------------------- v.1.0.0 -------------------------------------------|    "
"    HARNOMETIC is an application that allows you to change the signal frequency of audio files in any    "
"    format, and then upload the modified file to your device.                                            "
"                                                                                                         "
"                                                                                                         "
"    Open source code to explore                                                                          "





import sys
from PyQt5.QtWidgets import QApplication
from player import MediaPlayer


def _main():
    app = QApplication(sys.argv)
    app.setApplicationName("Harnometic | by sou1toon | v1.0.0")
    app.setApplicationVersion("1.0.0")
    
    app.setStyle('Fusion')
    
    player = MediaPlayer()
    player.show()
    
    sys.exit(app.exec_())
    
def closeEvent(self, event):
    if hasattr(self, 'equalizer_widget'): self.equalizer_widget.cleanup_temp_files()
    super().closeEvent(event)


if __name__ == "__main__": _main()