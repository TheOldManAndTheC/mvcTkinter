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

# Radiobutton base widget
# New functionality:
# - Notifies the controller and observing objects when the button is invoked
# - Allows state handling with setState()

from tkinter import ttk
from ...core import constants as mtk
from ...core.MVCWidget import MVCWidget


class Radiobutton(MVCWidget, ttk.Radiobutton):
    def __init__(self, parent=None, **options):
        ttk.Radiobutton.__init__(self, parent)
        self.command = None
        # the MVCWidget.__init__ has a call to our overridden configure()
        super().__init__(parent, **options)
        # if no command was set from the config in MVCWidget.__init__, make
        # sure the actual command is still set to _buttonPressed()
        if self.command is None:
            self.config(command=self._buttonPressed)

    def setState(self, state, key=None):
        self["state"] = state

    def _buttonPressed(self):
        if self.command is not None:
            self.command()
        self._notifyObservers(self, mtk.BUTTON_PRESSED)

    # In order to handle multiple observers we preserve the command which will
    # be executed in buttonPressed(), and set the actual command to
    # buttonPressed().
    def configure(self, cnf=None, **kw):
        if "command" in kw and kw["command"] != self._buttonPressed:
            self.command = kw["command"]
            kw["command"] = self._buttonPressed
        elif cnf is not None and "command" in cnf and \
                cnf["command"] != self._buttonPressed:
            self.command = cnf["command"]
            cnf["command"] = self._buttonPressed
        return super().configure(cnf, **kw)

    config = configure
