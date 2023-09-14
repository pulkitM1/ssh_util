from shell_util.platforms.unix import Unix as UnixPlatform


class Unix(UnixPlatform):
    download_dir = "~/Downloads"
    default_install_dir = "/Applications/Couchbase Server.app"

    # Non-root params
    nonroot_download_dir = download_dir
    nonroot_install_dir = default_install_dir
