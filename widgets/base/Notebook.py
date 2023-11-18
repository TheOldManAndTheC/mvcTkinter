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

# Notebook base widget
# New functionality:
# - Notifies the controller and observing objects when the button is invoked
# - Allows selected tab index getting and setting with value()/setValue()
# - Allows state handling of the notebook and tabs with setState()

from tkinter import ttk
from ...core import constants as mtk
from ...core.MVCWidget import MVCWidget


class Notebook(MVCWidget, ttk.Notebook):
    def __init__(self, parent=None, **options):
        ttk.Notebook.__init__(self, parent)
        super().__init__(parent, **options)
        self._binding = \
            self.bind("<<NotebookTabChanged>>",
                      lambda *_: self._notifyObservers(self, mtk.TAB_CHANGED))
        # don't do a reset here because there are no tabs at the start

    def value(self, key=None):
        # use the numeric index rather than the window path
        return self.index(self.select())

    def setValue(self, value, key=None):
        if value is not None and value < self.index("end"):
            self.select(value)

    # allow for specifying certain tabs
    def setState(self, state, key=None):
        # whole widget
        if key is None:
            self["state"] = state
            return
        # single tab
        if isinstance(key, str | int):
            self.tab(key, state=state)
            return
        # list or range of tab_ids/indices
        if isinstance(key, list | range):
            for tab in key:
                self.tab(tab, state=state)
            return

    def destroy(self) -> None:
        self.unbind("<<NotebookTabChanged>>", self._binding)
        super().destroy()
