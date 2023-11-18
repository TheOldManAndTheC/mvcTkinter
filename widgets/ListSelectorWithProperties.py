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

# ListSelectorWithProperties widget
# New options:
# dataReturn, properties
# A ListSelector that operates on a dictionary that can display properties
# within the dictionary as appended tags to the key items
# The format for the properties should be:
# "properties" = {
#   propertyKey: {
#       "tag": " (format {} aware string to be appended to displayed entry)"
#       "buttonText": (string, only inlcude if a button to manage the property
#           is desired)
#       "tooltip": (tooltip string, only include if buttonText is set)
#       ... (other properties may be included for the controller to operate on)
#   }
# }
# If there is a {} in the tag string, the value of the property will be shown.
# If there is a button, the controller object and observers will be notified
# that the property should be managed when it is pressed.
# The dataReturn option allows specifying a default dictionary of data to be
# associated with this selector.

from functools import partial
import tkinter as tk
import tkinter.simpledialog as sd
from ..core import constants as mtk
from .base.Button import Button
from .ListSelector import ListSelector

validDialogArgs = ["title", "prompt", "minvalue", "maxvalue", "initialvalue"]


class ListSelectorWithProperties(ListSelector):
    def __init__(self, parent=None, **options):
        super().__init__(parent, **options)
        self._properties = self.option("properties", dict())
        # if there are properties that need a toggle button, create them
        for propertyKey in self._properties:
            propertyEntry = self._properties[propertyKey]
            if "buttonText" not in propertyEntry:
                continue
            if "tooltip" in propertyEntry:
                tooltip = propertyEntry["tooltip"]
            else:
                tooltip = None
            # using a lambda here would end up with all buttons using the last
            # propertyKey in the loop, so use partial instead
            Button(self._filterFrame, text=propertyEntry["buttonText"],
                   command=partial(self._buttonPressed, propertyKey),
                   tooltip=tooltip, packSide=tk.LEFT)
        self._dataReturn = self.option("dataReturn")
        self.refresh()

    def value(self, key=None):
        match key:
            # want to get the keys from the source and not the display text
            case mtk.SELECTED_ITEMS:
                itemList = self._filteredItems()
                selected = []
                for index in self.value(mtk.SELECTION):
                    selected.append(itemList[index])
                return selected
            case mtk.PROPERTIES:
                return self._properties
            case mtk.DATA_RETURN:
                return self._dataReturn
        return super().value(key)

    def refresh(self):
        # need this because the superclass init calls this method, and it does
        # not have a properties attribute
        if not hasattr(self, "_properties"):
            super().refresh()
            return
        source = self.value(mtk.SOURCE)
        properties = self.value(mtk.PROPERTIES)
        displayList = []
        for key in self._filteredItems():
            displayText = key
            for propertyKey in properties:
                if propertyKey in source[key] and \
                        "tag" in properties[propertyKey]:
                    displayText += properties[propertyKey]["tag"]\
                        .format(source[key][propertyKey])
            displayList.append(displayText)
        self._listVar.set(displayList)

    def _buttonPressed(self, propertyKey):
        selections = self.value(mtk.SELECTED_ITEMS)
        if not selections:
            return
        propertyEntry = self.value(mtk.PROPERTIES)[propertyKey]
        dialogArgs = {"parent": self}
        for key in propertyEntry:
            if key in validDialogArgs:
                dialogArgs[key] = propertyEntry[key]
        propertyType = propertyEntry["propertyType"]
        value = None
        match propertyType:
            case "str":
                value = sd.askstring(**dialogArgs)
                if not value:
                    value = None
            case "int":
                value = sd.askinteger(**dialogArgs)
            case "float":
                value = sd.askfloat(**dialogArgs)
        if value is None and propertyType != "bool":
            return
        invalidKey = None
        for selection in selections:
            if not self._valueFromController(
                    mtk.LIST_SELECTOR_PROPERTY_VALIDATE,
                    propertyKey=propertyKey,
                    selection=selection,
                    value=value
            ):
                invalidKey = "invalid"
                continue
            entry = self.value(mtk.SOURCE)[selection]
            if propertyType == "bool":
                if propertyKey in entry:
                    entry.pop(propertyKey)
                else:
                    entry[propertyKey] = True
            elif value is None:
                if propertyKey in entry:
                    entry.pop(propertyKey)
            else:
                entry[propertyKey] = value
        self.refresh()
        self._notifyObservers(self, mtk.LIST_SELECTOR_PROPERTY_BUTTON_PRESSED,
                              invalidKey, propertyKey=propertyKey)
