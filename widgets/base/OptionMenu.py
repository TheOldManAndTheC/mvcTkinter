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

# Labelframe base widget
# New functionality:
# - Creates a StringVar to hold the selected option if one is not provided
# TODO:

from tkinter import ttk
from ...core.MVCWidget import MVCWidget
from ...widgets.base.StringVar import StringVar


class OptionMenu(MVCWidget, ttk.OptionMenu):
    def __init__(self, parent=None, **options):
        self.variable = self.option("variable", StringVar(self))
        ttk.OptionMenu.__init__(self, parent, self.variable)
        super().__init__(parent, **options)
        ...
