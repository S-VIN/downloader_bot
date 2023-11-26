import asyncio
import settings


class ConfirmationTimer:
    __confirmation_period__ = settings.DEFAULT_CONFIRMATION_PERIOD  # in seconds
    __media_counter__ = 0
    __callback__ = None  # коллбек, вызывается, когда таймер заканчивается
    __task__ = None

    def __init__(self, callback):
        self.__callback__ = callback

    async def __run_timer__(self):
        await asyncio.sleep(self.__confirmation_period__)
        await self.__callback__(self.__media_counter__)
        self.__media_counter__ = 0

    async def set_timer(self):
        if self.__confirmation_period__ is not None:

            # если уже был таймер - отменяем его
            try:
                self.__task__.cancel()
            except AttributeError:
                pass

            self.__task__ = asyncio.ensure_future(self.__run_timer__())

            try:
                await self.__task__
            except asyncio.CancelledError:
                pass

    def enable_confirmation(self, confirmation_period=settings.DEFAULT_CONFIRMATION_PERIOD):
        self.__confirmation_period__ = confirmation_period

    def disable_confirmation(self):
        self.__confirmation_period__ = None

    def increase_media_counter(self):
        self.__media_counter__ += 1
