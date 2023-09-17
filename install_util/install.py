import logging
import time
import sys

from install_util.install_lib.helper import InstallHelper
from install_util.install_lib.node_helper import NodeInstaller, NodeInstallInfo
from install_util.test_input import TestInputParser
from shell_util.remote_connection import RemoteMachineShellConnection


def start_and_wait_for_threads(thread_list, timeout):
    okay = True
    for tem_thread in thread_list:
        tem_thread.start()

    for tem_thread in thread_list:
        tem_thread.join(timeout)
        okay = okay and tem_thread.result
    return okay


def main(logger):
    helper = InstallHelper(logger)
    args = helper.parse_command_line_args(sys.argv[1:])
    logger.setLevel(args.log_level.upper())
    user_input = TestInputParser.get_test_input(args)

    for server in user_input.servers:
        server.install_status = "not_started"

    logger.info("Node health check")
    if not helper.check_server_state(user_input.servers):
        return 1

    # Objects for each node to track the URLs / state to reuse
    node_helpers = [
        NodeInstallInfo(
            server,
            helper.get_os(
                RemoteMachineShellConnection.get_info_for_server(server)),
            args.version, args.edition)
        for server in user_input.servers]

    logger.info("Validate os_type across servers")
    okay = helper.validate_server_status(node_helpers)
    if not okay:
        return 1

    logger.info("Populating build url to download")
    if args.url:
        for node_helper in node_helpers:
            node_helper.build_url = args.url
    else:
        tasks_to_run = ["populate_build_url"]
        if args.install_debug_info:
            tasks_to_run.append("populate_debug_build_url")

        url_builder_threads = \
            [NodeInstaller(logger, node_helper, tasks_to_run)
             for node_helper in node_helpers]
        okay = start_and_wait_for_threads(url_builder_threads, 60)
        if not okay:
            return 1

    logger.info("Downloading build")
    if args.skip_local_download:
        # Download on individual nodes
        download_threads = \
            [NodeInstaller(logger, node_helper, ["download_build"])
             for node_helper in node_helpers]
    else:
        # Local file download and scp to all nodes
        download_threads = [
            NodeInstaller(logger, node_helpers[0], ["local_download_build"])]
    okay = start_and_wait_for_threads(download_threads,
                                      args.build_download_timeout)
    if not okay:
        return 1

    install_tasks = args.install_tasks.split("-")
    logger.info("Starting installation tasks :: {}".format(install_tasks))
    install_threads = [
        NodeInstaller(logger, node_helper, install_tasks)
        for node_helper in node_helpers]
    okay = start_and_wait_for_threads(install_threads, args.timeout)
    if not okay:
        return 1
    return 0


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=logging.ERROR)
    log = logging.getLogger("install_util")

    start_time = time.time()
    exit_status = main(log)
    log.info("TOTAL INSTALL TIME = {0} seconds"
             .format(round(time.time() - start_time)))
    sys.exit(exit_status)
