from shell_util.platforms.windows import Windows as WindowsPlatform


class Windows(WindowsPlatform):
    download_dir = "/cygdrive/c/tmp/"
    default_install_dir = "/cygdrive/c/Program Files/Couchbase/Server"

    # Non-root params
    nonroot_download_dir = download_dir
    nonroot_install_dir = default_install_dir
