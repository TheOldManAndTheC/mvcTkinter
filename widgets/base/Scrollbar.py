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
# New options:
# axis, scrollWidget
# New functionality:
# - Allows direct attachment to scrollable widget with the axis and
#     scrollWidget options
# - Allows state handling with setState()
# Note: The axis and scrollWidget options will do nothing unless they are both
#   set.

import tkinter as tk
from tkinter import ttk
from ...core.MVCWidget import MVCWidget


class Scrollbar(MVCWidget, ttk.Scrollbar):
    def __init__(self, parent=None, **options):
        ttk.Scrollbar.__init__(self, parent)
        super().__init__(parent, **options)
        self._scrollWidget = self.option("scrollWidget")
        if self._scrollWidget is not None:
            match self.option("axis"):
                case tk.X:
                    self["orient"] = tk.HORIZONTAL
                    self["command"] = self._scrollWidget.xview
                    self._scrollWidget["xscrollcommand"] = self.set
                case tk.Y:
                    self["orient"] = tk.VERTICAL
                    self["command"] = self._scrollWidget.yview
                    self._scrollWidget["yscrollcommand"] = self.set
