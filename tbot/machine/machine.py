import abc
import typing

Self = typing.TypeVar("Self", bound="Machine")


class Machine(typing.ContextManager):
    """Connect to a machine (host, board, etc.)."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Name of this machine."""
        pass

    @abc.abstractmethod
    def destroy(self) -> None:
        """Destroy and cleanup this machine."""
        pass

    def __init__(self) -> None:
        """Connect to this machine."""
        self._rc = 0

    def __enter__(self: Self) -> Self:
        self._rc += 1
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore
        """Cleanup this machine instance."""
        self._rc -= 1
        if self._rc == 0:
            self.destroy()


class InteractiveMachine(abc.ABC):
    """Machine that can be used interactively."""

    @abc.abstractmethod
    def interactive(self) -> None:
        """
        Drop into an interactive shell on this machine.

        :raises RuntimeError: If TBot was not able to reacquire the shell
            after the session finished.
        """
        pass
