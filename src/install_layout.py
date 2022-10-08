import math
import sys
from typing import List

import termuxgui as tg
import termuxgui.oo as tgo
from activity import PackageActivity
from pm import PM, Package


_pagesize = 20

class InstallLayout(tgo.LinearLayout):

    def on_back(self):
        self.selected = []
        self.searchtext.settext("")
        self.a.set_active(self.a.main)
    
    def on_pkg_list(self, l, err):
        self.pgklist = l
        self.update_filter(None, None)
    
    def update_filter(self, e: tg.Event | None, v):
        text = self.searchtext.gettext()
        if isinstance(v, tgo.Checkbox):
            v.checked = e.value["set"]
        self.filteredlist = []
        for p in self.pgklist:
            if not self.exact.checked:
                if text in p:
                    self.filteredlist.append(p)
            else:
                if text == p:
                    self.filteredlist.append(p)
        self.max_page = math.floor(len(self.filteredlist) / _pagesize)
        self.set_page(0)
        self.a.hidesoftkeyboard()
    
    def on_next(self, e, v):
        if self.page < self.max_page:
            self.set_page(self.page + 1)

    def on_prev(self, e, v):
        if self.page > 0:
            self.set_page(self.page - 1)

    def on_install(self, e, v):
        if len(self.selected) == 0:
            return
        self.a.set_active(self.a.install_progress)
        self.a.install_progress.set_pm(self.pm, self.selected)
        self.selected = []
        for b in self.boxes:
            b.setchecked(False)
    
    def on_select(self, e: tg.Event, v: tgo.Checkbox):
        if v.gettext() == "":
            return
        if e.value["set"]:
            self.selected.append(v.gettext())
        else:
            self.selected.remove(v.gettext())
    
    def set_page(self, p):
        self.page = p
        nextbox = 0
        for p in self.filteredlist[self.page*_pagesize:(self.page+1)*_pagesize]:
            self.boxes[nextbox].settext(p)
            if p in self.selected:
                self.boxes[nextbox].setchecked(True)
            else:
                self.boxes[nextbox].setchecked(False)
            nextbox += 1
        while nextbox < len(self.boxes):
            self.boxes[nextbox].settext("")
            self.boxes[nextbox].setchecked(False)
            nextbox += 1
        pass
    
    def set_pm(self, pm: PM):
        self.pm = pm
        self.pgklist = []
        self.pkgrequest = pm.list_packages()
        self.pkgrequest.set_callback(self.on_pkg_list)

    def __init__(self, a: PackageActivity):
        super().__init__(a, a.frame, visibility=tgo.View.GONE)
        self.a = a
        self.pm: PM | None = None
        self.selected: List[str] = []
        self.pgklist: List[str] = []
        self.filteredlist: List[str] = []
        self.page = 0
        self.max_page = 0
        
        self.setmargin(10)

        self.bar = tgo.LinearLayout(self.a, self, vertical=False)
        self.bar.setheight(tgo.View.WRAP_CONTENT)
        self.bar.setlinearlayoutparams(0)
        self.bar.setmargin(10, "bottom")
        
        self.searchtext = tgo.EditText(self.a, "", self.bar)
        
        self.searchbutton = tgo.Button(self.a, "Search", self.bar)
        self.searchbutton.setwidth(tgo.View.WRAP_CONTENT)
        self.searchbutton.setlinearlayoutparams(0)
        self.searchbutton.on_click = self.update_filter
        
        self.installbutton = tgo.Button(self.a, "Install", self.bar)
        self.installbutton.on_click = self.on_install

        self.optionsbar = tgo.LinearLayout(self.a, self, vertical=False)
        self.optionsbar.setheight(tgo.View.WRAP_CONTENT)
        self.optionsbar.setlinearlayoutparams(0)
        self.optionsbar.setmargin(10, "bottom")
        
        self.exact = tgo.Checkbox(self.a, "Exact", self.optionsbar)
        self.exact.on_click = self.update_filter
        
        self.bar2 = tgo.LinearLayout(self.a, self, vertical=False)
        self.bar2.setheight(tgo.View.WRAP_CONTENT)
        self.bar2.setlinearlayoutparams(0)
        self.bar2.setmargin(10, "bottom")

        self.prev = tgo.Button(self.a, "Previous", self.bar2)
        self.prev.on_click = self.on_prev
        self.next = tgo.Button(self.a, "Next", self.bar2)
        self.next.on_click = self.on_next
        
        self.scroll = tgo.NestedScrollView(self.a, self)
        self.scrolllayout = tgo.LinearLayout(self.a, self.scroll)
        
        self.boxes: List[tgo.Checkbox] = []
        
        for i in range(0, _pagesize):
            box = tgo.Checkbox(self.a, "", self.scrolllayout)
            box.on_click = self.on_select
            self.boxes.append(box)
        
        
        
        
        
        
        

    pass
