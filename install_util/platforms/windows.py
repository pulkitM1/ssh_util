from install_util.constants.windows import WindowsConstants
from shell_util.platforms.windows import Windows as WindowsPlatform


class Windows(WindowsPlatform, WindowsConstants):
    def __init__(self, test_server, info=None):
        super(Windows, self).__init__(test_server, info)
