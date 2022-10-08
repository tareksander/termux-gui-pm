from typing import Optional

import termuxgui as tg
import termuxgui.oo as tgo
import pms
from pm import PM


class PackageActivity(tgo.Activity):
    
    def set_active(self, active: tgo.ViewGroup):
        self.active.setvisibility(tgo.View.GONE)
        self.active = active
        self.active.setvisibility(tgo.View.VISIBLE)
    
    def on_back(self):
        if hasattr(self.active, "on_back"):
            self.active.on_back()
    
    def intercept_back(self) -> bool:
        return True

    def __init__(self, c: tgo.Connection, t: Optional[tg.Task]):
        super().__init__(c, t)
        
        self.pms = pms.get()
        self.pm: PM | None = None
        
        self.frame = tgo.FrameLayout(self)
        
        from mainlayout import MainLayout
        self.main = MainLayout(self)
        
        from install_layout import InstallLayout
        self.install = InstallLayout(self)
        
        from install_progress_layout import InstallProgressLayout
        self.install_progress = InstallProgressLayout(self)
        
        from uninstall_layout import UninstallLayout
        self.uninstall = UninstallLayout(self)
        
        from uninstall_progress_layout import UninstallProgressLayout
        self.uninstall_progress = UninstallProgressLayout(self)
        
        from update_layout import UpdateLayout
        self.update = UpdateLayout(self)
        
        from upgrade_layout import UpgradeLayout
        self.upgrade = UpgradeLayout(self)
        
        self.active: tgo.ViewGroup = self.main

