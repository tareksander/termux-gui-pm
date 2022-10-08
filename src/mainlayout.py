import sys
import time

import termuxgui as tg
import termuxgui.oo as tgo
from activity import PackageActivity


class MainLayout(tgo.LinearLayout):

    def on_back(self):
        sys.exit(0)
    
    def on_itemselected(self, e: tg.Event, s: tgo.Spinner):
        for pm in self.a.pms:
            if pm.name == e.value["selected"]:
                self.a.pm = pm
                break
    
    def on_install(self, e: tg.Event, s: tgo.View):
        self.a.set_active(self.a.install)
        self.a.install.set_pm(self.a.pm)

    def on_uninstall(self, e: tg.Event, s: tgo.View):
        self.a.set_active(self.a.uninstall)
        self.a.uninstall.set_pm(self.a.pm)

    def on_update(self, e: tg.Event, s: tgo.View):
        self.a.set_active(self.a.update)
        self.a.update.set_pm(self.a.pm)

    def on_upgrade(self, e: tg.Event, s: tgo.View):
        self.a.set_active(self.a.upgrade)
        self.a.upgrade.set_pm(self.a.pm)
    
    def __init__(self, a: PackageActivity):
        super().__init__(a, a.frame)
        self.a = a
        
        self.setmargin(10)
        
        self.bar = tgo.LinearLayout(self.a, self, vertical=False)
        self.bar.setheight(tgo.View.WRAP_CONTENT)
        self.bar.setlinearlayoutparams(0)
        self.bar.setmargin(20, "bottom")
        
        self.pm_text = tgo.TextView(self.a, "Package manager: ", self.bar)
        self.pm_text.setwidth(tgo.View.WRAP_CONTENT)
        self.pm_text.setlinearlayoutparams(0)
        self.pm_text.setmargin(10, "right")
        
        self.pm_spinner = tgo.Spinner(self.a, self.bar)
        self.pm_spinner.on_itemselected = self.on_itemselected
        self.pm_spinner.setlist(list(map(lambda pm: pm.name, self.a.pms)))
        
        self.install = tgo.Button(self.a, "Install", self)
        self.install.setheight(tgo.View.WRAP_CONTENT)
        self.install.setlinearlayoutparams(0)
        self.install.on_click = self.on_install

        self.uninstall = tgo.Button(self.a, "Uninstall", self)
        self.uninstall.setheight(tgo.View.WRAP_CONTENT)
        self.uninstall.setlinearlayoutparams(0)
        self.uninstall.on_click = self.on_uninstall

        self.update = tgo.Button(self.a, "Update", self)
        self.update.setheight(tgo.View.WRAP_CONTENT)
        self.update.setlinearlayoutparams(0)
        self.update.on_click = self.on_update

        self.upgrade = tgo.Button(self.a, "Upgrade", self)
        self.upgrade.setheight(tgo.View.WRAP_CONTENT)
        self.upgrade.setlinearlayoutparams(0)
        self.upgrade.on_click = self.on_upgrade

        
        

        
        
        
        
        
        
        
        
        
    
    
    pass
