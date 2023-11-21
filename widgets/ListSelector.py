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

# ListSelector widget
# A bundle of widgets that implements a filterable listbox selector.
# Note: The source must be an iterable containing strings.
# New options:
# filter, filterButton, filterButtonTooltip, filterLabel, filterTooltip, source

import tkinter as tk
from ..core import constants as mtk
from ..core.Tooltip import Tooltip
from .base.Frame import Frame
from .base.StringVar import StringVar
from .base.Label import Label
from .base.Button import Button
from .base.Entry import Entry
from .base.Variable import Variable
from .base.Listbox import Listbox
from .base.Scrollbar import Scrollbar

defaultOptions = {
    "filterLabel": "Filter:",
    "filterTooltip": "Enter text to filter the display of items in the "
                     "panel below.",
    "filterButton": "Clear Filter",
    "filterButtonTooltip": "Clear the filter for this pane."
}

packTop = {"packAnchor": tk.NW, "packSide": tk.TOP}
packLeft = {"packSide": tk.LEFT}
packRight = {"packSide": tk.RIGHT}
packBottom = {"packSide": tk.BOTTOM}
fillX = {"packFill": tk.X}
fillY = {"packFill": tk.Y}
fillBoth = {"packFill": tk.BOTH}
expand = {"packExpand": True}
padx10 = {"packPadx": 10}


class ListSelector(Frame):
    def __init__(self, parent=None, **options):
        super().__init__(parent, **options)
        self.addDefaultOptions(defaultOptions)
        self._labelVar = StringVar(self, value=self.option(mtk.LABEL, ""))
        self._label = Label(self, textvariable=self._labelVar,
                            **(packTop | fillX))
        # need to apply the tooltip only to the header label
        if self._tooltip is not None:
            self._tooltip.bindTooltip(self._label)
        self._filterFrame = None
        self._filterVar = None
        self._filterEntry = None
        self._filterBinding = None
        # frame for the selection filter and property toggle buttons
        if self.option("filter", True):
            self._filterFrame = Frame(self, **(packTop | fillX))
            self._filterVar = StringVar(self)
            self._filterVar.registerObserver(self)
            filterLabel = Label(self._filterFrame,
                                text=self.option("filterLabel"), **packLeft)
            Tooltip(filterLabel, text=self.option("filterTooltip"))
            self._filterEntry = Entry(self._filterFrame,
                                      textvariable=self._filterVar,
                                      **(packLeft | fillX | expand))
            self._filterBinding = self._filterEntry.bind(
                "<Escape>",
                lambda *_: self.setValue("", mtk.FILTER),
                add="+"
            )
            Tooltip(self._filterEntry, text=self.option("filterTooltip"))
            clearFilterButton = Button(
                self._filterFrame,
                text=self.option("filterButton"),
                command=lambda *_: self.setValue("", mtk.FILTER),
                **(packLeft | padx10)
            )
            Tooltip(clearFilterButton, text=self.option("filterButtonTooltip"))
        self._listboxFrame = Frame(self, **(packTop | fillBoth | expand))
        self._listVar = Variable(self, value=[])
        self.listbox = Listbox(self._listboxFrame, listvariable=self._listVar,
                               **(packLeft | fillBoth | expand))
        self.listbox.config(self.optionsForTkWidget(self.listbox))
        self.listbox.registerObserver(self)
        self._yscrollbar = Scrollbar(self._listboxFrame,
                                     scrollWidget=self.listbox, axis=tk.Y,
                                    **(packRight | fillY))
        self._xscrollbar = Scrollbar(self, scrollWidget=self.listbox, axis=tk.X,
                                    **(packBottom | fillX))
        self._source = None
        self.setValue(self.option(mtk.SOURCE), mtk.SOURCE)

    def value(self, key=None):
        match key:
            case mtk.LABEL:
                return self._labelVar.get()
            case mtk.SELECTION | mtk.SELECTED_ITEMS:
                return self.listbox.value(key)
            case mtk.SOURCE:
                return self._source
            case mtk.FILTER:
                return self._filterVar.get()
        return None

    def setValue(self, value, key=None):
        match key:
            case mtk.LABEL:
                self._labelVar.set(value)
            case mtk.SOURCE:
                self._source = value
                self.setValue(None, mtk.SELECTION_CLEAR)
                self.refresh()
            case mtk.SELECTION_ANCHOR | mtk.SELECTION_CLEAR | \
                 mtk.SELECTION_SET:
                self.listbox.setValue(value, key)
            case mtk.FILTER:
                if self._filterVar is not None:
                    if value is None:
                        value = ""
                    self._filterVar.set(value)

    def refresh(self):
        self._listVar.set(self._filteredItems())

    def reset(self):
        self.setValue(self._valueFromController(mtk.SOURCE), mtk.SOURCE)

    def widgetUpdated(self, widget, event=None, key=None, **kwargs):
        if widget == self.listbox:
            self._notifyObservers(self, mtk.SELECTION_CHANGED)
        else:
            self.refresh()

    def destroy(self) -> None:
        self.listbox.unregisterObserver(self)
        if self._filterVar is not None:
            self._filterVar.unregisterObserver(self)
        if self._filterBinding is not None:
            self._filterEntry.unbind("<Escape>", self._filterBinding)
        super().destroy()

    def _filteredItems(self):
        if self._filterVar is not None:
            textFilter = self._filterVar.get()
        else:
            textFilter = ""
        itemList = []
        source = self.value(mtk.SOURCE)
        if source is not None:
            for item in self.value(mtk.SOURCE):
                if not textFilter.lower() in item.lower():
                    continue
                itemList.append(item)
        return itemList

    # Listbox method signatures from tkinter __init__.py
    def see(self, index):
        self.listbox.see(index)
