# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from contextvars import ContextVar
from sys import version_info

from opentelemetry.context.context import Context, _RuntimeContext

if (3, 5, 3) <= version_info < (3, 7):
    import aiocontextvars  # type: ignore # pylint:disable=import-error

    aiocontextvars  # pylint:disable=pointless-statement

elif (3, 4) < version_info <= (3, 5, 2):
    import opentelemetry.context.aiocontextvarsfix  # pylint:disable=wrong-import-position

    opentelemetry.context.aiocontextvarsfix  # pylint:disable=pointless-statement


class ContextVarsRuntimeContext(_RuntimeContext):
    """An implementation of the RuntimeContext interface which wraps ContextVar under
    the hood. This is the prefered implementation for usage with Python 3.5+
    """

    _CONTEXT_KEY = "current_context"

    def __init__(self) -> None:
        self._current_context = ContextVar(
            self._CONTEXT_KEY, default=Context()
        )

    def attach(self, context: Context) -> object:
        """Sets the current `Context` object. Returns a
        token that can be used to reset to the previous `Context`.

        Args:
            context: The Context to set.
        """
        return self._current_context.set(context)

    def get_current(self) -> Context:
        """Returns the current `Context` object. """
        return self._current_context.get()

    def detach(self, token: object) -> None:
        """Resets Context to a previous value

        Args:
            token: A reference to a previous Context.
        """
        self._current_context.reset(token)  # type: ignore


__all__ = ["ContextVarsRuntimeContext"]
