import logging


class CentOS(object):
    pass


class CentOS7(CentOS):
    def __init__(self, shell):
        super(CentOS7, self).__init__()

        self.shell = shell
        self.log = logging.getLogger("install_util")

    def is_ntp_installed(self):
        ntp_installed = False
        do_install = False
        self.log.info("Check if ntp is installed")
        os_version = "centos 7"
        output, e = self.shell.execute_command("systemctl status ntpd")
        for line in output:
            try:
                line = line.decode()
            except AttributeError:
                pass
            if "Active: active (running)" in line:
                ntp_installed = True
        if not ntp_installed:
            self.log.info("ntp not installed yet or not run.\n"
                          "Let remove any old one and install ntp")
            self.shell.execute_command("yum erase -y ntp", debug=False)
            self.shell.execute_command("yum install -y ntp", debug=False)
            self.shell.execute_command("systemctl start ntpd", debug=False)
            self.shell.execute_command("systemctl enable ntpd", debug=False)
            do_install = True
        # Check if ntp time sync didn't happened
        ntpstatoutput, _ = self.shell.execute_command("ntpstat")
        ntpstat = "".join(ntpstatoutput)
        timeoutput, _ = self.shell.execute_command("timedatectl status")
        self.log.debug("{} - {}".format(self.shell.ip, timeoutput))
        is_ntp_sync = "".join(timeoutput)
        if "unsynchronised" in ntpstat or "NTP synchronized: no" in is_ntp_sync:
            self.log.info("%s - Forcing ntp time sync as time is out of sync"
                          % self.shell.ip)
            self.shell.execute_command(
                "systemctl stop ntpd; ntpd -gq; systemctl start ntpd",
                debug=False)

        timezone, _ = self.shell.execute_command("date")
        timezone0 = timezone[0]
        if "PST" not in timezone0:
            self.shell.execute_command(
                "timedatectl set-timezone America/Los_Angeles",
                debug=False)

        if do_install:
            output, e = self.shell.execute_command("systemctl status ntpd")
            for line in output:
                if "Active: active (running)" in line:
                    self.log.info("%s - ntp is installed and running"
                                  % self.shell.ip)
                    ntp_installed = True
                    break

        output, _ = self.shell.execute_command("date", debug=False)
        self.log.info("\n{0} IP: {1}".format(output, self.shell.ip))
        if not ntp_installed and "centos" in os_version:
            mesg = "\n===============\n"\
                   "        This server {0} \n"\
                   "        failed to install ntp service.\n"\
                   "===============\n".format(self.shell.ip)
            # CBQE-6470: Continue with install by skipping the process
            # kill in case some issue with ntp setup
            self.log.info(mesg)
