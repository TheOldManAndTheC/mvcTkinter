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

# Text base widget
# New options:
# enableEdit
# New functionality:
# - Notifies the controller and observing objects when the button is invoked
# - Allows text value getting and setting with value()/setValue()
# - Allows enabling/disabling of user editing with enableEdit option/value key

import tkinter as tk
from ...core import constants as mtk
from ...core.MVCWidget import MVCWidget


class Text(MVCWidget, tk.Text):
    def __init__(self, parent=None, **options):
        tk.Text.__init__(self, parent)
        super().__init__(parent, **options)
        self._binding = None
        self._enableEdit = True
        self.setValue(self.option("enableEdit", True), mtk.ENABLE_EDIT)

    def value(self, key=None):
        match key:
            case mtk.ENABLE_EDIT:
                return self._enableEdit
            case mtk.TEXT | None:
                return self.get(1.0, "end-1c")
        return None

    def setValue(self, value, key=None):
        match key:
            case mtk.ENABLE_EDIT:
                if value is None:
                    value = False
                self._enableEdit = value
                if value and self._binding is not None:
                    self.unbind("<Key>", self._binding)
                    self._binding = None
                elif not value and self._binding is None:
                    self._binding = self.bind("<Key>", lambda e: "break")
            case mtk.TEXT | None:
                self.delete(1.0, tk.END)
                if value is not None:
                    self.insert(1.0, value)

    def destroy(self) -> None:
        self.setValue(True, mtk.ENABLE_EDIT)
        super().destroy()
