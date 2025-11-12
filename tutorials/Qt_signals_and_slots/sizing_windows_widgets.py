import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
)


class MainWindow(QMainWindow):
    """Responsive window with minimize/maximize/fullscreen controls.

    - Uses layouts and QSizePolicy so widgets adapt when the window resizes.
    - Provides buttons to Minimize, Toggle Maximize/Restore, and Toggle Fullscreen.
    - Adjusts the main label font size on resize as a simple responsive example.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            "Dashboard for International Maritime Vessel Monitoring and Trajectory Prognostics Automation System (IMVMPTAS)"
        )

        # Start at 80% of available screen size for a nicer default on different displays
        screen = QApplication.primaryScreen()
        if screen is not None:
            avail = screen.availableGeometry()
            start_w = int(avail.width() * 0.8)
            start_h = int(avail.height() * 0.8)
            self.resize(start_w, start_h)
        else:
            self.resize(1000, 700)

        # Central widget and layout
        central = QWidget()
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # A big label to illustrate dynamic resizing
        self.label = QLabel("Welcome to IMVMPTAS Dashboard")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setWordWrap(True)

        # Controls row
        controls = QHBoxLayout()
        btn_min = QPushButton("Minimize")
        btn_max = QPushButton("Maximize / Restore")
        btn_full = QPushButton("Fullscreen")

        btn_min.clicked.connect(self.on_minimize)
        btn_max.clicked.connect(self.on_toggle_maximize)
        btn_full.clicked.connect(self.on_toggle_fullscreen)

        # Put controls in layout
        controls.addWidget(btn_min)
        controls.addWidget(btn_max)
        controls.addWidget(btn_full)

        # Add widgets to main layout
        main_layout.addLayout(controls)
        main_layout.addWidget(self.label, stretch=1)

        self.setCentralWidget(central)

        # Minimum/maximum sizes are fine to keep if you want them, but not required
        self.setMinimumSize(QSize(400, 250))
        self.setMaximumSize(QSize(3000, 2000))

        # Track whether we are in fullscreen for toggling
        self._is_fullscreen = False

        # Initial font sizing
        self._update_label_font()

    def on_minimize(self):
        self.showMinimized()

    def on_toggle_maximize(self):
        # Toggle between normal and maximized window state
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def on_toggle_fullscreen(self):
        # Toggle fullscreen (different from maximized)
        if self._is_fullscreen:
            self.showNormal()
            self._is_fullscreen = False
        else:
            self.showFullScreen()
            self._is_fullscreen = True

    def resizeEvent(self, event):
        # Called on resize; update UI responsively
        super().resizeEvent(event)
        self._update_label_font()

    def _update_label_font(self):
        # Simple heuristic: base font size on the smaller of width/height
        w = max(100, self.width())
        h = max(60, self.height())
        size = int(min(w / 20, h / 10))
        size = max(10, min(size, 48))
        f = QFont()
        f.setPointSize(size)
        f.setBold(True)
        self.label.setFont(f)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


