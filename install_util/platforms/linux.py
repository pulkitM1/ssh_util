from shell_util.platforms.linux import Linux as LinuxPlatform


class Linux(LinuxPlatform):
    download_dir = "/tmp"
    default_install_dir = "/opt/couchbase"

    # Non-root params
    nonroot_download_dir = "/home/nonroot"
    nonroot_install_dir = "%s/cb/opt/couchbase" % nonroot_download_dir
