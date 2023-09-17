from threading import Thread

import install_util.constants
from install_util.constants import BuildUrlConstants
from shell_util.remote_connection import RemoteMachineShellConnection


class NodeInstallInfo(object):
    def __init__(self, server, os_type, version, edition):
        self.server = server
        self.os_type = os_type

        self.version = version
        self.edition = edition

        self.build_url = None
        self.debug_build_url = None
        self.non_root_package_mgr = None

        self.state = "not_started"


class NodeInstaller(Thread):
    def __init__(self, logger, node_install_info, steps):
        super(NodeInstaller, self).__init__()
        self.log = logger
        self.node_install_info = node_install_info
        self.steps = steps
        self.result = True

    def __construct_build_url(self, is_debuginfo_build=False):
        build_version = self.node_install_info.version.split("-")
        os_type = self.node_install_info.os_type
        node_info = RemoteMachineShellConnection.get_info_for_server(
            self.node_install_info.server)
        # Decide between release / regular build URL path
        if len(build_version) == 1:
            # Release build url
            url_path = "http://{}/{}/{}" \
                .format(BuildUrlConstants.CB_DOWNLOAD_SERVER,
                        BuildUrlConstants.CB_RELEASE_URL_PATH,
                        build_version[0])
        else:
            # Build_number specific url
            main_version = ".".join(build_version[0].split(".")[:2])
            # Reference: builds/latestbuilds/couchbase-server/trinity/1000
            url_path = "http://{}/{}/{}/{}" \
                .format(BuildUrlConstants.CB_DOWNLOAD_SERVER,
                        BuildUrlConstants.CB_LATESTBUILDS_URL_PATH,
                        BuildUrlConstants.CB_VERSION_NAME[main_version],
                        build_version[1])

        build_version = "-".join(build_version)

        file_prefix = "{}-{}" \
            .format(BuildUrlConstants.CB_BUILD_FILE_PREFIX,
                    self.node_install_info.edition)

        if os_type in install_util.constants.X86:
            # couchbase-server-enterprise-7.1.5-linux.x86_64.rpm
            # couchbase-server-enterprise-debuginfo-7.1.5-linux.x86_64.rpm
            if is_debuginfo_build:
                file_prefix = "{}-{}".format(file_prefix, "debuginfo")

            os_type = "linux"
            if float(build_version[:3]) < 7.1:
                os_type = self.node_install_info.os_type
            file_name = "{}-{}-{}.{}.{}" \
                .format(file_prefix,
                        build_version,
                        os_type,
                        node_info.architecture_type,
                        node_info.deliverable_type)
        elif os_type in install_util.constants.LINUX_AMD64:
            # TODO: Check install_utils.py L1127 redundant code presence
            # couchbase-server-enterprise_7.1.5-linux_amd64.deb
            # couchbase-server-enterprise-dbg_7.1.5-linux_amd64.deb
            if is_debuginfo_build:
                file_prefix = "{}-{}".format(file_prefix, "dbg")

            os_type = "linux"
            if float(build_version[:3]) < 7.1:
                os_type = self.node_install_info.os_type
            file_name = "{}_{}-{}_{}.{}" \
                .format(file_prefix,
                        build_version,
                        os_type,
                        "amd64",
                        node_info.deliverable_type)
        elif os_type in install_util.constants.WINDOWS_SERVER:
            # couchbase-server-enterprise_6.5.0-4557-windows_amd64.msi
            if "windows" in self.node_install_info.os_type:
                self.node_install_info.deliverable_type = "msi"
            file_name = "{}_{}-{}_{}.{}" \
                .format(file_prefix,
                        build_version,
                        self.node_install_info.os_type,
                        "amd64",
                        node_info.deliverable_type)
        elif os_type in install_util.constants.MACOS_VERSIONS:
            # couchbase-server-enterprise_6.5.0-4557-macos_x86_64.dmg
            file_name = "{}_{}-{}_{}-{}.{}" \
                .format(file_prefix,
                        build_version,
                        "macos",
                        node_info.architecture_type,
                        "unnotarized",
                        node_info.deliverable_type)
        else:
            raise Exception("Unsupported os_type '{}' for build_url"
                            .format(self.node_install_info.os_type))
        return "{}/{}".format(url_path, file_name)

    def populate_build_url(self):
        self.node_install_info.build_url = self.__construct_build_url()
        self.log.info("{} - Build url :: {}"
                      .format(self.node_install_info.server.ip,
                              self.node_install_info.build_url))

    def populate_debug_build_url(self):
        self.node_install_info.debug_build_url = self.__construct_build_url(
            is_debuginfo_build=True)
        self.log.info("{} - Debug build url :: {}"
                      .format(self.node_install_info.server.ip,
                              self.node_install_info.debug_build_url))

    def download_build_locally(self):
        pass

    def download_build(self):
        pass

    def download_debug_info_build(self):
        pass

    def run(self):
        for step in self.steps:
            self.log.info("{} - Running '{}'"
                          .format(self.node_install_info.server.ip, step))
            if step == "populate_build_url":
                # To download the main build url
                self.populate_build_url()
            elif step == "populate_debug_build_url":
                # To download the debug_info build url for backtraces
                self.populate_debug_build_url()
            elif step == "local_download_build":
                self.download_build_locally()
            elif step == "download_build":
                self.download_build()
                if self.node_install_info.debug_build_url:
                    self.download_debug_info_build()
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
