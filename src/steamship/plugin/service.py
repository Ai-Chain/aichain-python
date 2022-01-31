from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

from steamship.base.response import RemoteError, Task

T = TypeVar('T')
U = TypeVar('U')


@dataclass
class PluginRequest(Generic[T]):
    data: T = None


@dataclass
class PluginResponse(Generic[U]):
    error: RemoteError = None
    task: Task[U] = None
    data: U = None


class PluginService(ABC):
    @abstractmethod
    def _run_one(self, request: PluginRequest[T]) -> PluginResponse[U]:
        pass

    def run_one(self, request: PluginRequest[T]) -> PluginResponse[U]:
        try:
            return self._run_one(request)
        except RemoteError as remote_error:
            return PluginResponse[U](error=remote_error)
        except Exception as error:
            return PluginResponse[U](error=RemoteError(
                message="Unhandled exception completing your request",
                error=error
            ))
