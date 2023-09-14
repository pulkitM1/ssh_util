from threading import Thread

from install_util.constants import BuildUrlConstants


class NodeInstallInfo(object):
    def __init__(self, server, version):
        self.server = server
        self.common_url_path = None
        self.build_url = None
        self.debug_build_url = None
        self.non_root_package_mgr = None
        self.version = version
        self.state = ""


class NodeInstaller(Thread):
    def __init__(self, logger, node_install_info, steps):
        super(NodeInstaller, self).__init__()
        self.log = logger
        self.node_info = node_install_info
        self.steps = steps
        self.result = True

    def __populate_build_url(self):
        build_version = self.node_info.version.split("-")
        # Check if the given build is release build
        if len(build_version) == 1:
            # Release build url
            url_path = "builds/releases/{}".format(build_version[0])
        else:
            # Build_number specific url
            main_version = ".".join(build_version[0].split(".")[:2])
            # Reference: builds/latestbuilds/couchbase-server/trinity/1000
            url_path = "builds/latestbuilds/couchbase-server/{}/{}" \
                .format(BuildUrlConstants.CB_VERSION_NAME[main_version],
                        build_version[1])

        self.node_info.common_url_path = \
            "http://{}/{}" \
            .format(BuildUrlConstants.CB_DOWNLOAD_SERVER,
                    url_path)

    def __populate_debug_build_url(self):
        pass

    def __download_build_locally(self):
        pass

    def __download_build(self):
        pass

    def __download_debug_info_build(self):
        pass

    def run(self):
        for step in self.steps:
            self.log.info("{} - Running '{}'"
                          .format(self.node_info.server.ip, step))
            if step == "populate_url":
                # To download the main build url
                self.__populate_build_url()
            elif step == "populate_debug_build_url":
                # To download the debug_info build url for backtraces
                self.__populate_debug_build_url()
            elif step == "local_download_build":
                self.__download_build_locally()
            elif step == "download_build":
                self.__download_build()
                if self.node_info.debug_build_url:
                    self.__download_debug_info_build()
            elif step == "uninstall":
                pass
            elif step == "deep_cleanup":
                pass
            elif step == "pre_install":
                pass
            elif step == "install":
                pass
            elif step == "post_install":
                pass
            elif step == "post_install_cleanpup":
                pass
            else:
                self.result = False
