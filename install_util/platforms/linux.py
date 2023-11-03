from install_util.constants.linux import LinuxConstants
from shell_util.platforms.linux import Linux as LinuxPlatform


class Linux(LinuxPlatform, LinuxConstants):
    def __init__(self, test_server, info=None):
        super(Linux, self).__init__(test_server, info)
