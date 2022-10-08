import subprocess
from typing import List

import re
from pm import PM, Package, Request, SubprocessRequest


def list_processor(inp: str) -> List[str]:
    return inp.splitlines()


def extract_details(ret: str) -> Package:
    name = re.search(r"Package: (.*)", ret)
    if name is not None:
        name = name.group(1)
    desc = re.search(r"Description: (.*(?:\n .*)*)", ret)
    if desc is not None:
        desc = desc.group(1)
    ver = re.search(r"Version: (.*)", ret)
    if ver is not None:
        ver = ver.group(1)
    main = re.search(r"Maintainer: (.*)", ret)
    if main is not None:
        main = main.group(1)
    dep = re.search(r"Depends: (.*)", ret)
    if dep is not None:
        dep = dep.group(1)
        dep = dep.split(", ")
    return Package(name, desc, ver, main, dep)


class APT(PM):
    
    def __init__(self, name: str):
        super().__init__(name)
    
    def details(self, p: str) -> Package:
        return extract_details(str(subprocess.run(["apt-cache", "show", "--no-all-versions", p], stdout=subprocess.PIPE, close_fds=True).stdout, "ascii"))
    
    def list_packages(self) -> Request[List[str]]:
        return SubprocessRequest(["apt-cache", "pkgnames"], list_processor)
    
    def list_installed(self) -> Request[List[str]]:
        return SubprocessRequest(["apt-mark", "showmanual"], list_processor)

    def install(self, p: str) -> Request[None]:
        return SubprocessRequest(["apt-get", "-y", "install", p], lambda inp: None)

    def uninstall(self, p: str) -> Request[None]:
        return SubprocessRequest(["apt-get", "-y", "remove", p], lambda inp: None)

    def fetch(self) -> Request[None]:
        return SubprocessRequest(["apt-get", "update"], lambda inp: None)

    def upgrade(self) -> Request[None]:
        return SubprocessRequest(["apt-get", "-y", "upgrade"], lambda inp: None)


