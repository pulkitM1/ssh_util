from argparse import ArgumentParser

from install_util.constants import SUPPORTED_OS
from shell_util.remote_connection import RemoteMachineShellConnection


class InstallHelper(object):
    def __init__(self, logger):
        self.log = logger

    def check_server_state(self, servers):
        result = True
        reachable = list()
        unreachable = list()
        for server in servers:
            try:
                shell = RemoteMachineShellConnection(server)
                shell.disconnect()
                reachable.append(server.ip)
            except Exception as e:
                self.log.error(e)
                unreachable.append(server.ip)

        if len(unreachable) > 0:
            self.log.info("-" * 100)
            for server in unreachable:
                self.log.error("INSTALL FAILED ON: \t{0}".format(server))
            self.log.info("-" * 100)
            for server in reachable:
                self.log.info("INSTALL COMPLETED ON: \t{0}".format(server))
            self.log.info("-" * 100)
            result = False
        return result

    @staticmethod
    def parse_command_line_args(arguments):
        parser = ArgumentParser(description="Installer for Couchbase-Server")
        parser.add_argument("--install_tasks",
                            help="List of tasks to run '-' separated",
                            default="uninstall-install-init-cleanup")
        parser.add_argument("-i", "--ini", dest="ini",
                            help="Ini file path",
                            required=True)

        parser.add_argument("-v", "--version", dest="version",
                            help="Build version to be installed",
                            required=True)
        parser.add_argument("--edition", default="enterprise",
                            help="CB edition",
                            choices=["enterprise", "community"])
        parser.add_argument("--url", default="",
                            help="Specific URL to use for build download")
        parser.add_argument("--storage_mode", default="plasma",
                            help="Sets indexer storage mode")
        parser.add_argument("--enable_ipv6", default=False,
                            help="Enable ipv6 mode in ns_server",
                            action="store_true")
        parser.add_argument("--install_debug_info",
                            dest="install_debug_info", default=False,
                            help="Flag to install debug package for debugging",
                            action="store_true")
        parser.add_argument("--skip_local_download",
                            dest="skip_local_download", default=False,
                            help="Download build individually on each node",
                            action="store_true")

        parser.add_argument("--timeout", default=300,
                            help="End install after timeout seconds")
        parser.add_argument("--build_download_timeout", default=300,
                            help="Timeout for build download. "
                                 "Usefull during slower download envs")
        parser.add_argument("--params", "-p", dest="params",
                            help="Other install params")
        parser.add_argument("--log_level", default="info",
                            help="Logging level",
                            choices=["info", "debug", "error", "critical"])

        return parser.parse_args(arguments)

    @staticmethod
    def get_os(info):
        os = info.distribution_version.lower()
        to_be_replaced = ['\n', ' ', 'gnu/linux']
        for _ in to_be_replaced:
            if _ in os:
                os = os.replace(_, '')
        if info.deliverable_type == "dmg":
            major_version = os.split('.')
            os = major_version[0] + '.' + major_version[1]
        if info.distribution_type == "Amazon Linux 2":
            os = "amzn2"
        return os

    def validate_server_status(self, node_helpers):
        result = True
        known_os = set()
        for node_helper in node_helpers:
            curr_os = node_helper.os_type
            if node_helper.os_type not in SUPPORTED_OS:
                self.log.critical("{} - Unsupported os: {}"
                                  .format(server.ip, node_helper.os_type))
                result = False
            else:
                known_os.add(node_helper.os_type)

        if len(known_os) != 1:
            result = False
        return result
