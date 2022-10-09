import subprocess
from typing import List

import re
from pm import PM, Package, Request, SubprocessRequest


def list_processor(inp: str) -> List[str]:
    return inp.splitlines()


def extract_details(ret: str) -> Package:
    name = re.search(r"^Name\s*: (\S+)", ret, re.MULTILINE)
    if name is not None:
        name = name.group(1)
    desc = re.search(r"^Description\s*: (.+)", ret, re.MULTILINE)
    if desc is not None:
        desc = desc.group(1)
    ver = re.search(r"^Version\s*: (\S+)", ret, re.MULTILINE)
    if ver is not None:
        ver = ver.group(1)
    main = re.search(r"^Packager\s*: (\S+)", ret, re.MULTILINE)
    if main is not None:
        main = main.group(1)
    dep = re.search(r"^Depends On\s*: ([^:]+)(?=\n)(?![^\n]+:)", ret, re.MULTILINE)
    if dep is not None:
        dep = dep.group(1)
        dep = re.sub("\\s+", " ", dep)
        dep = dep.split(" ")
    return Package(name, desc, ver, main, dep)


class Pacman(PM):
    
    def __init__(self, name: str):
        super().__init__(name)
    
    def details(self, p: str) -> Package:
        return extract_details(str(subprocess.run(["pacman", "-Si", p], stdout=subprocess.PIPE, close_fds=True).stdout, "ascii"))
    
    def list_packages(self) -> Request[List[str]]:
        return SubprocessRequest(["pacman", "-Slq"], list_processor)
    
    def list_installed(self) -> Request[List[str]]:
        return SubprocessRequest(["pacman", "-Qqe"], list_processor)

    def install(self, p: str) -> Request[None]:
        return SubprocessRequest(["pacman", "-S", "--noconfirm", p], lambda inp: None)

    def uninstall(self, p: str) -> Request[None]:
        return SubprocessRequest(["pacman", "-Rs", "--noconfirm", p], lambda inp: None)

    def fetch(self) -> Request[None]:
        return SubprocessRequest(["pacman", "-Sy"], lambda inp: None)

    def upgrade(self) -> Request[None]:
        return SubprocessRequest(["pacman", "-Syu", "--noconfirm"], lambda inp: None)


