from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NT2QT

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent = None, dpi = 300):
        fig = Figure(dpi = dpi)
        self.axes = fig.add_subplot(111)
        fig.subplots_adjust(left = 0.11, bottom = 0.125, right = 0.95, top = 0.95)
        super().__init__(fig)

class NavigationToolbar2QT(NT2QT):
        NT2QT.toolitems = (
            ('Home', 'Восстановить вид', 'home', 'home'),
            ('Back', 'Предыдущий вид', 'back', 'back'),
            ('Forward', 'Следующий вид', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Переместить', 'move', 'pan'),
            ('Zoom', 'Увеличить', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            )
