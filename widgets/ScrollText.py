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

# ScrollText widget
# Convenience class for the common use case of a text widget and vertical
# scrollbar.
# TODO: add horizontal scrollbar? show/hide scrollbars?

import tkinter as tk
from .base.Frame import Frame
from .base.Text import Text
from .base.Scrollbar import Scrollbar


textOptions = {
    "packSide": tk.LEFT,
    "packFill": tk.BOTH,
    "packExpand": True,
}

scrollbarOptions = {
    "axis": tk.Y,
    "packSide": tk.LEFT,
    "packFill": tk.Y,
}


class ScrollText(Frame):
    def __init__(self, parent=None, **options):
        super().__init__(parent, **options)
        self.text = Text(self, **textOptions)
        self.text.config(self.optionsForTkWidget(self.text))
        self.scrollbar = Scrollbar(self, scrollWidget=self.text,
                                   **scrollbarOptions)

    def value(self, key=None):
        return self.text.value()

    def setValue(self, value, key=None):
        self.text.setValue(value, key)

    # Text method signatures from tkinter __init__.py
    def bbox(self, index):
        return self.text.bbox(index)

    def compare(self, index1, op, index2):
        return self.text.compare(index1, op, index2)

    def count(self, index1, index2, *args):
        return self.text.count(index1, index2, *args)

    def debug(self, boolean=None):
        return self.text.debug(boolean)

    def delete(self, index1, index2=None):
        self.text.delete(index1, index2)

    def dlineinfo(self, index):
        return self.text.dlineinfo(index)

    def dump(self, index1, index2=None, command=None, **kw):
        return self.text.dump(index1, index2, command, **kw)

    def edit(self, *args):
        return self.text.edit(*args)

    def edit_modified(self, arg=None):
        return self.text.edit_modified(arg)

    def edit_redo(self):
        return self.text.edit_redo()

    def edit_reset(self):
        return self.text.edit_reset()

    def edit_separator(self):
        return self.text.edit_separator()

    def edit_undo(self):
        return self.text.edit_undo()

    def get(self, index1, index2=None):
        return self.text.get(index1, index2)

    def image_cget(self, index, option):
        return self.text.image_cget(index, option)

    def image_configure(self, index, cnf=None, **kw):
        return self.text.image_configure(index, cnf, **kw)

    def image_create(self, index, cnf={}, **kw):
        return self.text.image_create(index, cnf, **kw)

    def image_names(self):
        return self.text.image_names()

    def index(self, index):
        return self.text.index(index)

    def insert(self, index, chars, *args):
        self.text.insert(index, chars, *args)

    def mark_gravity(self, markName, direction=None):
        return self.text.mark_gravity(markName, direction)

    def mark_names(self):
        return self.text.mark_names()

    def mark_set(self, markName, index):
        self.text.mark_set(markName, index)

    def mark_unset(self, *markNames):
        self.text.mark_unset(*markNames)

    def mark_next(self, index):
        return self.text.mark_next(index)

    def mark_previous(self, index):
        return self.text.mark_previous(index)

    def peer_create(self, newPathName, cnf={}, **kw):
        self.text.peer_create(newPathName, cnf, **kw)

    def peer_names(self):
        return self.text.peer_names()

    def replace(self, index1, index2, chars, *args):
        self.text.replace(index1, index2, chars, *args)

    def scan_mark(self, x, y):
        self.text.scan_mark(x, y)

    def scan_dragto(self, x, y):
        self.text.scan_dragto(x, y)

    def search(self, pattern, index, stopindex=None, forwards=None,
               backwards=None, exact=None, regexp=None, nocase=None,
               count=None, elide=None):
        return self.text.search(pattern, index, stopindex, forwards, backwards,
                                exact, regexp, nocase, count, elide)

    def see(self, index):
        self.text.see(index)

    def tag_add(self, tagName, index1, *args):
        self.text.tag_add(tagName, index1, *args)

    def tag_unbind(self, tagName, sequence, funcid=None):
        self.text.tag_unbind(tagName, sequence, funcid)

    def tag_bind(self, tagName, sequence, func, add=None):
        return self.text.tag_bind(tagName, sequence, func, add)

    def tag_cget(self, tagName, option):
        return self.text.tag_cget(tagName, option)

    def tag_configure(self, tagName, cnf=None, **kw):
        return self.text.tag_configure(tagName, cnf, **kw)

    tag_config = tag_configure

    def tag_delete(self, *tagNames):
        self.text.tag_delete(*tagNames)

    def tag_lower(self, tagName, belowThis=None):
        self.text.tag_lower(tagName, belowThis)

    def tag_names(self, index=None):
        return self.text.tag_names(index)

    def tag_nextrange(self, tagName, index1, index2=None):
        return self.text.tag_nextrange(tagName, index1, index2)

    def tag_prevrange(self, tagName, index1, index2=None):
        return self.text.tag_prevrange(tagName, index1, index2)

    def tag_raise(self, tagName, aboveThis=None):
        self.text.tag_raise(tagName, aboveThis)

    def tag_ranges(self, tagName):
        return self.text.tag_ranges(tagName)

    def tag_remove(self, tagName, index1, index2=None):
        self.text.tag_remove(tagName, index1, index2)

    def window_cget(self, index, option):
        return self.text.window_cget(index, option)

    def window_configure(self, index, cnf=None, **kw):
        return self.text.window_configure(index, cnf, **kw)

    window_config = window_configure

    def window_create(self, index, cnf={}, **kw):
        self.text.window_create(index, cnf, **kw)

    def window_names(self):
        return self.text.window_names()

    def yview_pickplace(self, *what):
        self.text.yview_pickplace(*what)
