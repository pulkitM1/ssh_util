from install_util.constants.unix import UnixConstants
from shell_util.platforms.unix import Unix as UnixPlatform


class Unix(UnixPlatform, UnixConstants):
    def __init__(self, test_server, info=None):
        super(Unix, self).__init__(test_server, info)
