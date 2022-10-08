import signal
import sys
import threading
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Callable
import subprocess


class Package:
    def __init__(self, name: str, description: str, version: str, maintainer: str, dependencies: List[str]):
        self.name = name
        self.description = description
        self.version = version
        self.maintainer = maintainer
        self.dependencies = dependencies


T = TypeVar("T")


class Request(ABC, Generic[T]):
    
    @abstractmethod
    def set_callback(self, callback: Callable[[T|None, str|None], None]):
        pass
    
    @abstractmethod
    def finished(self) -> bool:
        pass
    
    @abstractmethod
    def code(self) -> int | None:
        pass
    
    @abstractmethod
    def error(self) -> str | None:
        pass

    @abstractmethod
    def cancel(self) -> bool:
        pass
    
    @abstractmethod
    def result(self) -> T | None:
        pass


class SubprocessRequest(Request, Generic[T]):

    def _run(self):
        try:
            (out, err) = self.p.communicate()
            if self.p.returncode == 0:
                with self.lock:
                    self.out = self.processor(out)
                    if self.callback is not None:
                        self.callback(self.out, None)
                    self._is_finished = True
            else:
                with self.lock:
                    self.err = err
                    if self.callback is not None:
                        self.callback(None, self.err)
                    self._is_finished = True
        except BaseException as e:
            print(e, file=sys.stderr, flush=True)
            raise e

    def set_callback(self, callback: Callable[[T | None, str | None], None]):
        with self.lock:
            if self._is_finished:
                if self.err is not None:
                    callback(None, self.err)
                else:
                    callback(self.out, None)
            self.callback = callback

    def __init__(self, cmd: List[str], processor: Callable[[str], T], callback: Callable[[T | None, str | None], None] | None = None, shell=False):
        self.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True, encoding="ascii",
                                  shell=shell)
        self.out = None
        self.err = None
        self._is_finished = False
        self.lock = threading.Lock()
        self.processor = processor
        self.callback = callback
        self.t = threading.Thread(target=self._run)
        self.t.start()

    def finished(self) -> bool:
        return self.p.returncode is not None

    def code(self) -> int | None:
        return self.p.returncode

    def error(self) -> str | None:
        return self.err

    def cancel(self) -> bool:
        self.p.send_signal(signal.SIGINT)
        try:
            self.p.wait(0.5)
            return True
        except subprocess.TimeoutExpired:
            return False

    def result(self) -> T | None:
        return self.out


class PM(ABC):
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def list_packages(self) -> Request[List[str]]:
        pass

    @abstractmethod
    def list_installed(self) -> Request[List[str]]:
        pass

    @abstractmethod
    def details(self, p: str) -> Package:
        pass
    
    @abstractmethod
    def install(self, p: str) -> Request[None]:
        pass

    @abstractmethod
    def uninstall(self, p: str) -> Request[None]:
        pass
    
    @abstractmethod
    def fetch(self) -> Request[None]:
        pass
    
    @abstractmethod
    def upgrade(self) -> Request[None]:
        pass

