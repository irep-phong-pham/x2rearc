from .anonymous_base_controller import AnonymousBaseController

class HealthyController(AnonymousBaseController):
    def __init__(self):
        super().__init__()

    def get(self):
        return 'healthy'