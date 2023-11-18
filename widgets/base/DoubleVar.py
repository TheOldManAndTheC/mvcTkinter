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

# BooleanVar base class
# New functionality:
# - Notifies the controller and observing objects when the variable changes
# - Allows value getting and setting with value()/setValue()

import tkinter as tk
from ...core import constants as mtk
from ...core.MVCWidget import MVCWidget

varOptionKeys = ["container", "value", "name"]


class DoubleVar(MVCWidget, tk.DoubleVar):
    def __init__(self, parent=None, **options):
        varOptions = {key: options[key] for key in varOptionKeys
                      if key in options}
        tk.DoubleVar.__init__(self, **varOptions)
        super().__init__(parent, **options)
        self.trace_add("write",
                       lambda *_: self._notifyObservers(self,
                                                        mtk.VALUE_CHANGED))

    def value(self, key=None):
        return self.get()

    def setValue(self, value, key=None):
        if value is None:
            value = 0.0
        self.set(value)
