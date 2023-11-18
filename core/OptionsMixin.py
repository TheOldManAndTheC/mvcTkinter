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

# OptionsMixin mixin class
# Adds basic options and default options handling to subclasses.

class OptionsMixin:
    options = dict()
    # self.defaultOptions can be merged with other dictionaries of default
    # options by subclasses to be used by self.option
    defaultOptions = dict()

    # This method returns the options or default options value for the given
    # key, or a default value if one exists, otherwise None.
    def option(self, key, default=None):
        if key in self.options:
            return self.options[key]
        if key in self.defaultOptions:
            return self.defaultOptions[key]
        return default

    # This method returns a dictionary of options from the given keys.
    # If a key is not in the options or default options, it won't be added.
    # If the keys argument is a dictionary instead of a list, option keys
    # will be replaced by their dictionary values, unless they are None.
    def optionSet(self, keys):
        options = dict()
        for key in keys:
            if self.option(key) is not None:
                if isinstance(keys, dict) and keys[key] is not None:
                    newKey = keys[key]
                else:
                    newKey = key
                options[newKey] = self.option(key)
        return options

    # This method is a convenience method for subclasses to add more default
    # options.
    def addDefaultOptions(self, options):
        self.defaultOptions = self.defaultOptions | options
