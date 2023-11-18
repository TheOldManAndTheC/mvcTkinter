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

# ConsoleText widget
# Redirects stdout and stderr to a ScrollText widget and disables editing.
# New options:
# autoStart

import sys
import threading
import io
from ..core import constants as mtk
from .ScrollText import ScrollText


class ConsoleText(ScrollText):
    class _Redirector(io.TextIOBase):
        def __init__(self, text, pipe="stdOut"):
            super().__init__()
            self.text = text
            self.pipe = pipe
            self.lock = threading.Lock()

        def write(self, string):
            self.lock.acquire()
            self.text.insert("end", string, self.pipe)
            # output testing
            # sys.__stdout__.write(str(string))
            self.lock.release()
            self.text.see("end")
            self.text.update()

    def __init__(self, parent=None, **options):
        super().__init__(parent, **options)
        self.tag_config("stdErr", foreground="red")
        self.setValue(False, mtk.ENABLE_EDIT)
        self._savedStdOut = None
        self._savedStdErr = None
        self._redirecting = False
        if self.option("autoStart"):
            self.setValue(True, mtk.REDIRECT)

    def value(self, key=None):
        match key:
            case mtk.REDIRECT:
                return self._redirecting
        return super().value(key)

    def setValue(self, value, key=None):
        match key:
            case mtk.REDIRECT:
                if value and not self._redirecting:
                    self._savedStdOut = sys.stdout
                    self._savedStdErr = sys.stderr
                    sys.stdout = self._Redirector(self)
                    sys.stderr = self._Redirector(self, "stdErr")
                    self._redirecting = True
                elif not value and self._redirecting:
                    sys.stdout = self._savedStdOut
                    sys.stderr = self._savedStdErr
                    self._savedStdOut = None
                    self._savedStdErr = None
                    self._redirecting = False
                return
        super().setValue(value, key)

    def destroy(self) -> None:
        self.setValue(False, mtk.REDIRECT)
        super().destroy()
