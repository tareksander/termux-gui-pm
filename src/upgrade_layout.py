import sys

import termuxgui as tg
import termuxgui.oo as tgo
from activity import PackageActivity
from pm import PM, Request


class UpgradeLayout(tgo.LinearLayout):
    
    def callback(self, res, error):
        self.a.set_active(self.a.main)
    
    def on_back(self):
        self.a.c.toast("Cancelling upgrade", True)
        if self.request.cancel():
            self.a.set_active(self.a.main)

    def set_pm(self, pm: PM):
        self.pm = pm
        self.request = pm.upgrade()
        self.request.set_callback(self.callback)

    def __init__(self, a: PackageActivity):
        super().__init__(a, a.frame, visibility=tgo.View.GONE)
        self.a = a
        self.pm: PM | None = None
        self.request: Request[None] | None = None

        self.setmargin(10)

        self.text = tgo.TextView(self.a, "Updating packages", self)
