import math
import sys
from typing import List

import termuxgui as tg
import termuxgui.oo as tgo
from activity import PackageActivity
from pm import PM, Package, Request


class UninstallProgressLayout(tgo.LinearLayout):
    def install_next(self, res, err):
        if err is not None:
            self.a.c.toast("Error removing package")
            self.a.set_active(self.a.main)
            return
        if not self.cancel:
            self.uninstallindex += 1
            if len(self.selected) < self.uninstallindex:
                self.pm.uninstall(self.selected[self.uninstallindex]).set_callback(self.install_next)
            else:
                self.a.set_active(self.a.main)
        else:
            self.a.set_active(self.a.main)
    
    def on_back(self):
        self.a.c.toast("Cancelling uninstall", True)
        self.cancel = True
    
    def set_pm(self, pm: PM, selected: List[str]):
        self.pm = pm
        self.selected = selected
        self.cancel = False
        self.uninstallindex = 0
        string = "Uninstalling packages:\n"
        string += "\n".join(self.selected)
        self.text.settext(string)
        self.pm.uninstall(self.selected[self.uninstallindex]).set_callback(self.install_next)

    def __init__(self, a: PackageActivity):
        super().__init__(a, a.frame, visibility=tgo.View.GONE)
        self.a = a
        self.pm: PM | None = None
        self.selected: List[str] = []
        self.uninstallindex = 0
        self.cancel = False
        
        self.scroll = tgo.NestedScrollView(self.a, self)
        self.text = tgo.TextView(self.a, "", self.scroll)
        
        self.setmargin(10)

        
        
        
        
        
        
        

    pass
