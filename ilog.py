from abc import ABC, abstractmethod


class ILog(ABC):
    @abstractmethod
    async def write(self, message: str) -> None:
        pass

    @abstractmethod
    async def stop(self, immediate: bool = False) -> None:
        pass

    @abstractmethod
    async def wait_for_completion(self) -> None:
        pass