import logging


class Debian(object):
    def __init__(self, shell):
        self.log = logging.getLogger("install_util")
        self.shell = shell


class Debian10(Debian):
    def __init__(self, shell):
        super(Debian10, self).__init__(shell)

    def is_ntp_installed(self):
        ntp_installed = False
        do_install = False
        self.log.info("Check if ntp is installed")
        output, e = self.shell.execute_command("systemctl status ntp")
        if not output:
            self.log.info("%s - Installing ntp on the server" % self.shell.ip)
            self.shell.execute_command("apt-get install -y ntp", debug=False)
            self.shell.execute_command("systemctl start ntp", debug=False)
            self.shell.execute_command("/etc/init.d/ntpd start", debug=False)
            do_install = True
        elif output and "Active: inactive (dead)" in output[2]:
            log.info(
                "ntp is not running.  Let remove it and install again in {0}" \
                .format(self.ip))
            self.shell.execute_command("apt-get remove -y ntp", debug=False)
            self.shell.execute_command("apt-get install -y ntp", debug=False)
            self.shell.execute_command("systemctl start ntp", debug=False)
            # self.execute_command("ntpdate pool.ntp.org", debug=False)
            self.shell.execute_command("/etc/init.d/ntpd start", debug=False)
            do_install = True
        elif output and "active (running)" in output[2]:
            ntp_installed = True
        timezone, _ = self.shell.execute_command("date")
        if "PST" not in timezone[0]:
            self.shell.execute_command("cp /etc/localtime /root/old.timezone",
                                 debug=False)
            self.shell.execute_command("rm -rf /etc/localtime", debug=False)
            self.shell.execute_command(
                "ln -s /usr/share/zoneinfo/America/Los_Angeles "
                "/etc/localtime", debug=False)
        if do_install:
            output, e = self.shell.execute_command("systemctl status ntpd")
            if output and "active (running)" in output[2]:
                self.log.info("%s - ntp is installed and running"
                              % self.shell.ip)
                ntp_installed = True

        output, _ = self.execute_command("date", debug=False)
        log.info("\n{0} IP: {1}".format(output, self.ip))
        if not ntp_installed and "centos" in os_version:
            mesg = "\n===============\n" \
                   "        This server {0} \n" \
                   "        failed to install ntp service.\n" \
                   "===============\n".format(self.ip)
            # CBQE-6470: Continue with install by skipping the process kill in case some issue with ntp setup
            log.info(mesg)


class Debian11(object):
    def __init__(self, shell):
        super(Debian11, self).__init__(shell)

    def is_ntp_installed(self):
        ntp_installed = False
        do_install = False
        os_version = ""
        self.log.info("Check if ntp is installed")
