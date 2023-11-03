class LinuxConstants(object):
    download_dir = "/tmp"
    default_install_dir = "/opt/couchbase"

    # Non-root params
    nonroot_download_dir = "/home/nonroot"
    nonroot_install_dir = "%s/cb/opt/couchbase" % nonroot_download_dir

    local_download_dir = "/tmp"
    wget_cmd = "cd {} ; wget -Nq {}"
