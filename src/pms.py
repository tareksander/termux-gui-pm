from typing import List

import apt
import pacman
import pm
import proot_distro
import shutil
import os


def get() -> List[pm.PM]:
    pms = []
    package_format = os.getenv("TERMUX_MAIN_PACKAGE_FORMAT")
    if package_format is None:
        if shutil.which("apt") is not None:
            pms.append(apt.APT("Termux APT"))
        if shutil.which("pacman") is not None:
            pms.append(pacman.Pacman("Termux pacman"))
    else:
        if package_format == "debian":
            pms.append(apt.APT("Termux APT"))
        if package_format == "pacman":
            pms.append(pacman.Pacman("Termux pacman"))
    pms.extend(proot_distro.proot_pms())
    return pms


