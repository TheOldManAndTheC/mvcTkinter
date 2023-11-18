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

# Listbox base widget
# New functionality:
# - Notifies the controller and observing objects when the selection changes
# - Allows selection handling with value()/setValue()
# - Allows state handling with setState()

import tkinter as tk
from ...core import constants as mtk
from ...core.MVCWidget import MVCWidget


class Listbox(MVCWidget, tk.Listbox):
    def __init__(self, parent=None, **options):
        tk.Listbox.__init__(self, parent)
        super().__init__(parent, **options)
        self._binding = \
            self.bind("<<ListboxSelect>>",
                      lambda *_: self._notifyObservers(self,
                                                       mtk.SELECTION_CHANGED))

    def value(self, key=None):
        match key:
            case mtk.SELECTION:
                return self.curselection()
            case mtk.SELECTED_ITEMS:
                selected = []
                for index in self.curselection():
                    selected.append(self.get(index))
                return selected

    def setValue(self, value, key=None):
        match key:
            case mtk.SELECTION_ANCHOR:
                self.selection_anchor(value)
            case mtk.SELECTION_CLEAR:
                if value is None:
                    value = (0, tk.END)
                self.selection_clear(*value)
            case mtk.SELECTION_SET:
                self.selection_set(value)

    def setState(self, state, key=None):
        self["state"] = state

    def destroy(self) -> None:
        self.unbind("<<ListboxSelect>>", self._binding)
        super().destroy()
