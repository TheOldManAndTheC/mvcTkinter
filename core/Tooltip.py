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

# Tooltip class
# Displays a floating window with helpful text near the mouse cursor when it is
# above the parent widget.
# TODO: figure out removing bindings for garbage collection

import tkinter as tk
from tkinter import ttk

defaultOptions = {
    "background": "#FFFFF0",
    "borderwidth": 0,
    "delay": 300,
    "justify": tk.LEFT,
    "offsetX": 10,
    "offsetY": 5,
    "relief": tk.FLAT,
    "text": "Tooltip",
    "wraplength": 250,
}

packOptions = {
    "fill": tk.BOTH,
    "ipadx": 5,
    "ipady": 1,
}

tooltipBindings = {
    "<Enter>": True,
    "<Leave>": False,
    "<ButtonPress>": False,
    "<Key>": False,
}


class Tooltip:
    def __init__(self, parent, **options):
        self.options = defaultOptions | options
        self.labelOptions = self._getLabelOptions()
        self.parent = None
        self._bindings = dict()
        self.bindTooltip(parent)
        self._tooltip = None
        self._timer = None

    def _enterParent(self, *args):
        if self._timer:
            self.parent.after_cancel(self._timer)
        self._timer = self.parent.after(self.options["delay"],
                                        self.showTooltip)

    def _leaveParent(self, *args):
        if self._timer:
            self.parent.after_cancel(self._timer)
        self._timer = None
        self.hideTooltip()

    def showTooltip(self, useMouse=True):
        self._tooltip = tk.Toplevel()
        self._tooltip.wm_overrideredirect(True)
        label = ttk.Label(self._tooltip, **self.labelOptions)
        label.pack(packOptions)
        if useMouse:
            mouseX, mouseY = label.winfo_pointerxy()
        else:
            # use a virtual mouse pointer in the center of the parent widget
            mouseX = self.parent.winfo_rootx() + self.parent.winfo_width() / 2 \
                     - self.options["offsetX"]
            mouseY = self.parent.winfo_rooty() + self.parent.winfo_height() / 2\
                     - self.options["offsetY"]
        x = mouseX + self.options["offsetX"]
        y = mouseY + self.options["offsetY"]
        # Before checking for collision against the screen edges, move the
        # tooltip to the expected place. If the tooltip does need to be moved,
        # the update statement will cause the tooltip to briefly show on screen
        # before moving, so it's better if it's not in the upper left corner
        self._tooltip.wm_geometry("+%d+%d" % (x, y))
        # need to update after packing to get the correct width and height below
        self._tooltip.update_idletasks()
        # need to reference the tkinter label itself, not the label's frame
        if x + label.winfo_width() > label.winfo_screenwidth():
            x = mouseX - self.options["offsetX"] - label.winfo_width()
        if x < 0:
            x = 0
        if y + label.winfo_height() > label.winfo_screenheight():
            y = mouseY - self.options["offsetY"] - label.winfo_height()
        if y < 0:
            y = 0
        self._tooltip.wm_geometry("+%d+%d" % (x, y))

    def hideTooltip(self):
        if self._tooltip:
            self._tooltip.destroy()
        self._tooltip = None

    def _getLabelOptions(self):
        # just need a temporary label to get the config options
        label = ttk.Label()
        options = dict()
        for option in label.config():
            if option in self.options:
                options[option] = self.options[option]
        label.destroy()
        return options

    def bindTooltip(self, newParent=None):
        for event, isEnter in tooltipBindings.items():
            if event in self._bindings and self.parent is not None:
                self.parent.unbind(event, self._bindings[event])
                self._bindings.pop(event)
            if newParent is None:
                continue
            if isEnter:
                method = self._enterParent
            else:
                method = self._leaveParent
            self._bindings[event] = newParent.bind(event, method, add="+")
        self.parent = newParent
