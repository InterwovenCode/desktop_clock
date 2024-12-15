# 参考资料：
#   - [Animations and Transformations with QtQuick](https://www.pythonguis.com/tutorials/qml-animations-transformations/)
#   - [在线QML热更编辑器](https://patrickelectric.work/qmlonline/)
#   - [FigmaQML](https://github.com/mmertama/FigmaQML)

from plugin import *
from PyQt5.QtQuick import *
from PyQt5.QtQuickWidgets import *
from PyQt5.QtQml import *
from time import localtime
sys.path.insert(0, os.path.dirname(__file__))
from resource import *

class Backend(QObject):
    hms = pyqtSignal(int, int, int, arguments=['hours','minutes','seconds'])

    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.timer.setInterval(100)  # msecs 100 = 1/10th sec
        self.timer.timeout.connect(self.update_time)
        self.timer.start()

    def update_time(self):
        local_time = localtime()
        self.hms.emit(local_time.tm_hour, local_time.tm_min, local_time.tm_sec)

class DrawingScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        qmlUrl = "qrc:/desktop_clock/qml/main.qml"
        canvas_quick_item = CanvasQuickQmlItem(QRectF(0, 0, 200, 200), qmlUrl)
        canvas_quick_item.setFlags(
            QGraphicsItem.ItemIsSelectable
            | QGraphicsItem.ItemIsMovable
            | QGraphicsItem.ItemIsFocusable
        )
        canvas_quick_item.setAcceptHoverEvents(True)

        self.backend = Backend()
        canvas_quick_item.quickWidget.rootObject().setProperty("backend", self.backend)
        self.backend.update_time()
        self.addItem(canvas_quick_item)

class DrawingView(QGraphicsView):
    def __init__(self, scene: QGraphicsScene, parent=None):
        super().__init__(scene, parent)
        self.initUI()

    def initUI(self):
        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.HighQualityAntialiasing
            | QPainter.TextAntialiasing
            | QPainter.SmoothPixmapTransform
        )

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet(
            "background: transparent; border:0px; padding: 0px; margin: 0px;"
        )

        self.scene_width, self.scene_height = 64000, 64000
        self.scene().setSceneRect(
            -self.scene_width // 2,
            -self.scene_height // 2,
            self.scene_width,
            self.scene_height,
        )

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

class DesktopClockWindow3(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setWindowFlag(Qt.WindowType.WindowTransparentForInput, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)

        self.initUI()
        self.show()

        screen = QApplication.primaryScreen()
        availableGeometry = screen.availableGeometry()

        self.move(
            availableGeometry.width() - self.width(), 
            availableGeometry.height() - self.height(), 
                  )

    def initUI(self):
        self.setStyleSheet("QWidget { background-color: #E3212121; }")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scene = DrawingScene()
        view = DrawingView(self.scene)

        self.layout.addWidget(view)

    def paintEvent(self, a0: QPaintEvent) -> None:
        backgroundPath = QPainterPath()
        backgroundPath.setFillRule(Qt.WindingFill)

        return super().paintEvent(a0)

class DesktopClockWindow1(QQuickWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setClearColor(QColor(Qt.GlobalColor.transparent))

        self.setSource(QUrl("qrc:/desktop_clock/qml/main.qml"))

        self.backend = Backend()
        self.rootObject().setProperty("backend", self.backend)
        self.backend.update_time()

        screen = QApplication.primaryScreen()
        availableGeometry = screen.availableGeometry()
        self.move(
            availableGeometry.width() - self.width() - 12, 
            availableGeometry.height() - self.height() - 12, 
                  )

class DesktopClockWindow2(QQuickView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setFlag(Qt.WindowType.WindowTransparentForInput, True)
        self.setColor(QColor(Qt.GlobalColor.transparent))

        self.setSource(QUrl("qrc:/desktop_clock/qml/main.qml"))

        self.backend = Backend()
        self.rootObject().setProperty("backend", self.backend)
        self.backend.update_time()

        screen = QApplication.primaryScreen()
        availableGeometry = screen.availableGeometry()
        self.setPosition(
            availableGeometry.width() - self.width() - 12, 
            availableGeometry.height() - self.height() - 48, 
                  )


class DesktopClock(PluginInterface):
    def __init__(self):
        super().__init__()
        self.effectWnd = None
        self._runtimePath = os.path.dirname(os.path.abspath(__file__))
        pass
    
    @property
    def runtimePath(self):
        return self._runtimePath

    @property
    def previewImages(self) -> list:
        folderPath = os.path.join(self.runtimePath, "preview")
        images = glob.glob(f"{folderPath}/*.*", recursive=False)
        return images

    @property
    def name(self):
        return "DesktopClock"

    @property
    def displayName(self):
        return "桌面时钟"

    @property
    def desc(self):
        return "给桌面右下角添加一个时钟挂件"

    @property
    def author(self) -> str:
        return "yaoxuanzhi"

    @property
    def icon(self):
        return QIcon(self.runtimePath + "/icons/desktop_clock.svg")

    @property
    def version(self) -> str:
        return "v1.0.0"

    @property
    def url(self) -> str:
        return "https://github.com/InterwovenCode/desktop_clock"

    @property
    def tags(self) -> list:
        return ["clock"]

    def onChangeEnabled(self):
        if self.enable:
            QQuickWindow.setSceneGraphBackend(QSGRendererInterface.GraphicsApi.Software)
            self.effectWnd = DesktopClockWindow1()
            # self.effectWnd = DesktopClockWindow2()
            # self.effectWnd = DesktopClockWindow3()
            self.effectWnd.show()
        else:
            self.effectWnd.close()
            self.effectWnd = None