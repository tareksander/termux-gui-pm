import os
import shutil
import subprocess
from pathlib import Path
from typing import List
import re

import apt
import pacman
from pm import Request, SubprocessRequest, Package, PM

prefix = "/data/data/com.termux/files/usr"

plugindir = f"{prefix}/etc/proot-distro"
runtimedir = f"{prefix}/var/lib/proot-distro"
dlcachedir = f"{runtimedir}/dlcache"
installdir = f"{runtimedir}/installed-rootfs"

nameregex = "(?<=DISTRO_NAME=\")([^\n]+)(?=\")"


class ProotAPT(apt.APT):
    
    def __init__(self, name, distro):
        super().__init__(name)
        self.distro = distro
    
    def details(self, p: str) -> Package:
        return apt.extract_details(str(subprocess.run(["proot-distro", "login", "--isolated", self.distro, "--",
                                                       "apt-cache", "show", "--no-all-versions", p],
                                                      stdout=subprocess.PIPE, close_fds=True).stdout, "ascii"))

    def list_packages(self) -> Request[List[str]]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "apt-cache", "pkgnames"], apt.list_processor)

    def list_installed(self) -> Request[List[str]]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "apt-mark", "showmanual"], apt.list_processor)

    def install(self, p: str) -> Request[None]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "apt-get", "-y", "install", p], lambda inp: None)

    def uninstall(self, p: str) -> Request[None]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "apt-get", "-y", "remove", p], lambda inp: None)

    def fetch(self) -> Request[None]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "apt-get", "update"], lambda inp: None)

    def upgrade(self) -> Request[None]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "apt-get", "-y", "dist-upgrade"], lambda inp: None)


class ProotPacman(PM):

    def __init__(self, name: str, distro):
        super().__init__(name)
        self.distro = distro

    def details(self, p: str) -> Package:
        return pacman.extract_details(str(subprocess.run(["proot-distro", "login", "--isolated", self.distro, "--",
                                                          "pacman", "-Si", p], stdout=subprocess.PIPE, close_fds=True).stdout, "ascii"))

    def list_packages(self) -> Request[List[str]]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "pacman", "-Slq"], pacman.list_processor)

    def list_installed(self) -> Request[List[str]]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "pacman", "-Qqe"], pacman.list_processor)

    def install(self, p: str) -> Request[None]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "pacman", "-S", "--noconfirm", p], lambda inp: None)

    def uninstall(self, p: str) -> Request[None]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "pacman", "-Rs", "--noconfirm", p], lambda inp: None)

    def fetch(self) -> Request[None]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "pacman", "-Sy"], lambda inp: None)

    def upgrade(self) -> Request[None]:
        return SubprocessRequest(["proot-distro", "login", "--isolated", self.distro, "--", "pacman", "-Syu", "--noconfirm"], lambda inp: None)


def proot_pms() -> List[PM]:
    pms = []
    if os.path.exists(plugindir) and shutil.which("proot-distro") is not None:
        for plugin in Path(plugindir).iterdir():
            if plugin.suffix == ".sh":
                with plugin.open() as f:
                    m = re.search(nameregex, f.read())
                    if m is not None:
                        if os.path.isfile(installdir + "/" + plugin.stem + "/usr/bin/apt"):
                            pms.append(ProotAPT(m.group(1) + " APT", plugin.stem))
                        if os.path.isfile(installdir + "/" + plugin.stem + "/usr/bin/pacman"):
                            pms.append(ProotPacman(m.group(1) + " pacman", plugin.stem))
    return pms

