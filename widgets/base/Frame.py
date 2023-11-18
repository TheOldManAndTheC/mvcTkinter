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

# Checkbutton base widget
# New functionality:
# - Allows state handling with setState()
# - Allows recursive refreshing of child widgets with refresh()
# - Allows recursive resetting of child widgets with reset()

import tkinter as tk
from tkinter import ttk
from ...core.MVCWidget import MVCWidget


class Frame(MVCWidget, ttk.Frame):
    def __init__(self, parent=None, **options):
        if parent is None:
            parent = tk.Tk()
        ttk.Frame.__init__(self, parent)
        super().__init__(parent, **options)

    def setState(self, state, key=None):
        for widget in self.widgets.values():
            widget.setState(state, key)

    def refresh(self):
        for widget in self.widgets.values():
            widget.refresh()

    def reset(self):
        for widget in self.widgets.values():
            widget.reset()
