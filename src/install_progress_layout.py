import math
import sys
from typing import List

import termuxgui as tg
import termuxgui.oo as tgo
from activity import PackageActivity
from pm import PM, Package, Request


class InstallProgressLayout(tgo.LinearLayout):
    def install_next(self, res, err):
        if err is not None:
            self.a.c.toast("Error installing package")
            self.a.set_active(self.a.install)
            return
        if not self.cancel:
            self.installindex += 1
            if len(self.selected) < self.installindex:
                self.pm.install(self.selected[self.installindex]).set_callback(self.install_next)
            else:
                self.a.set_active(self.a.install)
        else:
            self.a.set_active(self.a.install)
    
    def on_back(self):
        self.a.c.toast("Cancelling install", True)
        self.cancel = True
    
    def set_pm(self, pm: PM, selected: List[str]):
        self.pm = pm
        self.selected = selected
        self.cancel = False
        self.installindex = 0
        string = "Installing packages:\n"
        string += "\n".join(self.selected)
        self.text.settext(string)
        self.pm.install(self.selected[self.installindex]).set_callback(self.install_next)

    def __init__(self, a: PackageActivity):
        super().__init__(a, a.frame, visibility=tgo.View.GONE)
        self.a = a
        self.pm: PM | None = None
        self.selected: List[str] = []
        self.installindex = 0
        self.cancel = False
        
        self.scroll = tgo.NestedScrollView(self.a, self)
        self.text = tgo.TextView(self.a, "", self.scroll)
        
        self.setmargin(10)

        
        
        
        
        
        
        

    pass
