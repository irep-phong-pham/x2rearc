from .anonymous_base_controller import AnonymousBaseController

class PerformanceController(AnonymousBaseController):
    def __init__(self):
        super().__init__()

    def get(self):
        return "performance"
