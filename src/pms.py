from typing import List

import apt
import pm
import proot_distro


def get() -> List[pm.PM]:
    pms = [apt.APT("Termux APT")]
    pms.extend(proot_distro.proot_pms())
    return pms


