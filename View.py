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

# View widget
# Implements a main view as a top level widget to work with a controller object.
# New options:
# minHeight, minWidth, title

from .core import constants as mtk
from .widgets.base.Frame import Frame

defaultOptions = {
    "title": "",
    "minWidth": 1,
    "minHeight": 1,
}


class View(Frame):
    def __init__(self, parent=None, **options):
        super().__init__(parent, **options)
        self.addDefaultOptions(defaultOptions)
        self.root = self.parent
        self.root.title(self.option("title"))
        self.root.minsize(width=self.option("minWidth"),
                          height=self.option("minHeight"))
        self._minGeometry = "{}x{}+0+0".format(self.option("minWidth"),
                                               self.option("minHeight"))
        self._lastGeometry = None
        self.setValue(self.controller().valueForWidget(self))
        self._binding = self.root.bind("<Configure>",
                                       lambda *_: self._windowGeometryChanged())

    def value(self, key=None):
        return self.root.geometry()

    def setValue(self, value, key=None):
        if value is not None and not value.startswith("1x1+"):
            self.root.geometry(value)
        else:
            self.root.geometry(self._minGeometry)
        self._lastGeometry = self.root.geometry()

    def _windowGeometryChanged(self):
        if self.root.geometry() == self._lastGeometry:
            return
        self._lastGeometry = self.root.geometry()
        # avoid writing bad geometry to the settings
        if self.root.geometry().startswith("1x1+"):
            return
        self._notifyObservers(self, mtk.GEOMETRY_CHANGED)

    def destroy(self) -> None:
        self.root.unbind("<Configure>", self._binding)
        super().destroy()
