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

# ListBuilder widget
# New options:
# builderButtonTooltip, selector, sources
# A bundle of tkinter widgets that implements a list builder.
# The left pane contains the list to be built, and the pane(s) on the right
# contain entries that can be added to the list.  A button between them adds
# and removes items from the list depending on what's selected.
# Note: selector and sources options must be set. Selector and sources (list)
#   must be dictionaries with name, source, label (optional),
#   properties (optional)

from copy import deepcopy
import tkinter as tk
from ..core import constants as mtk
from .base.Frame import Frame
from .base.Button import Button
from .ListSelectorWithProperties import ListSelectorWithProperties

defaultOptions = {
    "builderButtonTooltip": "If items are selected in the panel to the left, "
                            "they will be removed. If items are selected in "
                            "a panel to the right, they will be added to the "
                            "panel to the left."
}

left = {"packSide": tk.LEFT}
fillBoth = {"packFill": tk.BOTH}
expand = {"packExpand": True}
padX10 = {"packPadx": 10}


class ListBuilder(Frame):
    def __init__(self, parent=None, **options):
        super().__init__(parent, **options)
        self.addDefaultOptions(defaultOptions)
        self.sourceSelectors = dict()
        self.selector = self._selectorFromConfig(self,
                                                 self.option("selectorOptions"),
                                                 **left)
        self.selectButton = Button(
            self, text="<->", tooltip=self.option("builderButtonTooltip"),
            command=lambda *_: self._buttonPressed(),
            **(left | padX10)
        )
        sourcesFrame = Frame(self, **(left | fillBoth | expand))
        for sourceConfig in self.option("sourceOptions"):
            self.sourceSelectors[sourceConfig["name"]] = \
                self._selectorFromConfig(sourcesFrame, sourceConfig)
        self.refresh()

    def _selectorFromConfig(self, frame, config, packSide: object = tk.TOP):
        options = fillBoth | expand | {
            "controller": self._controller,
            "selectmode": tk.EXTENDED,
            "packSide": packSide,
            "packPady": 5,
        }
        options = options | config
        return ListSelectorWithProperties(frame, **options)

    def setValue(self, value, key=None):
        match key:
            case mtk.SELECTION_CLEAR:
                self.selector.setValue(value, key)
                for sourceName in self.sourceSelectors:
                    self.sourceSelectors[sourceName].setValue(value, key)

    def refresh(self):
        self.selector.refresh()
        for sourceName in self.sourceSelectors:
            self.sourceSelectors[sourceName].refresh()

    def reset(self):
        self.selector.reset()
        for sourceName in self.sourceSelectors:
            self.sourceSelectors[sourceName].reset()

    def _buttonPressed(self):
        source = self.selector.value(mtk.SOURCE)
        if source is None:
            return
        for selection in self.selector.value(mtk.SELECTED_ITEMS):
            if not self._valueFromController(
                    mtk.LIST_BUILDER_VALIDATE_REMOVE,
                    source=source,
                    selection=selection,
            ):
                continue
            if isinstance(source, list):
                source.remove(selection)
            else:
                source.pop(selection)
        selected = False
        invalidKey = None
        for sourceName in self.sourceSelectors:
            sourceSelector = self.sourceSelectors[sourceName]
            sourceSelectorSource = sourceSelector.value(mtk.SOURCE)
            for selection in sourceSelector.value(mtk.SELECTED_ITEMS):
                if selection in source:
                    continue
                if isinstance(source, list):
                    if not self._valueFromController(
                            mtk.LIST_BUILDER_VALIDATE_ADD,
                            source=sourceSelectorSource,
                            selection=selection,
                    ):
                        invalidKey = "invalid"
                        continue
                    source.append(selection)
                    selected = True
                else:
                    dataReturn = sourceSelector.value(mtk.DATA_RETURN)
                    if dataReturn is None:
                        dataReturn = deepcopy(sourceSelectorSource[selection])
                    else:
                        dataReturn = deepcopy(dataReturn)
                    if not self._valueFromController(
                            mtk.LIST_BUILDER_VALIDATE_ADD,
                            source=sourceSelectorSource,
                            selection=selection,
                            entry=dataReturn,
                    ):
                        invalidKey = "invalid"
                        continue
                    source[selection] = dataReturn
                    selected = True
        self.selector.refresh()
        if selected:
            self.selector.see(tk.END)
        self._notifyObservers(self, mtk.LIST_BUILDER_BUTTON_PRESSED, invalidKey)
