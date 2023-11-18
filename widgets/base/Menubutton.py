# Copyright (c) 2023 The Old Man and the C
#
# This file is part of mvcTkinter.
#
# mvcTkinter is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# mvcTkinter is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with mvcTkinter. If not, see <https://www.gnu.org/licenses/>.

# Menubutton base widget
# New options:
# menuData
# New functionality:
#  - Set up a menu with item entries with menuData
# TODO:

from tkinter import ttk
from ...core import constants as mtk
from ...core.MVCWidget import MVCWidget
from .StringVar import StringVar
from .Menu import Menu


class Menubutton(MVCWidget, ttk.Menubutton):
    def __init__(self, parent=None, **options):
        ttk.Menubutton.__init__(self, parent)
        self._variable = None
        self._trace = None
        super().__init__(parent, **options)
        if self._variable is None:
            self.config(textvariable=StringVar(self))
        if self.option("menuData") is not None:
            if "config" in self.option("menuData"):
                menuConfig = self.option("menuData")["config"]
            else:
                menuConfig = dict()
            menu = Menu(self, **menuConfig)
            for item in self.option("menuData")["items"]:
                if "config" in item:
                    itemConfig = item["config"]
                else:
                    itemConfig = {}
                if item["type"] == "radiobutton" and \
                        "variable" not in itemConfig:
                    itemConfig["variable"] = self._variable
                menu.add(item["type"], **itemConfig)
            self["menu"] = menu

    def value(self, key=None):
        match key:
            case "variable":
                return self._variable
        return self._variable.get()

    def setValue(self, value, key=None):
        if value is None:
            value = ""
        match key:
            case "variable":
                self.configure(textvariable=value)
                return
        self._variable.set(value)

    def setState(self, state, key=None):
        self["state"] = state

    def _registerVariable(self):
        if self._variable is None:
            return
        if issubclass(self._variable.__class__, MVCWidget):
            self._variable.registerObserver(self)
        else:
            self._trace = self._variable.trace_add(
                "write",
                lambda *_: self._notifyObservers(self, mtk.VALUE_CHANGED)
            )

    def _unregisterVariable(self):
        if self._trace is not None:
            self._variable.trace_remove("write", self._trace)
            self._trace = None
        elif self._variable is not None:
            self._variable.unregisterObserver(self)

    def configure(self, cnf=None, **kw):
        variable = None
        if "textvariable" in kw:
            variable = kw["textvariable"]
        elif cnf is not None and "textvariable" in cnf:
            variable = cnf["textvariable"]
        if variable is not None and self._variable != variable:
            self._unregisterVariable()
            self._variable = variable
            self._registerVariable()
        return super().configure(cnf, **kw)

    config = configure

    def destroy(self) -> None:
        self._unregisterVariable()
        super().destroy()
