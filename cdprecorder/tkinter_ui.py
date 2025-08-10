from __future__ import annotations

import tkinter as tk
import math
import time
import threading
from time import strftime
from tkinter import ttk
from tkinter import font as tkfont
from typing import TYPE_CHECKING

from twisted.internet import defer

from .user_interface import RecordControlUI

if TYPE_CHECKING:
    from typing import Any, Awaitable, Callable, Coroutine, Optional
    from twisted.internet.interfaces import IReactorTime


class RecorderButton(tk.Canvas):
    def __init__(
        self,
        master: tk.Widget,
        width: int = 60,
        height: int = 60,
        corner_radius: int = 14,
        **kwargs: object,
    ):
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)  # type: ignore[arg-type]
        self.width = width
        self.height = height
        self.corner_radius = corner_radius

        self.small_circ_rad_proc = 0.6

        self.is_started = False

        self._draw_rec()

        self.on_start: Optional[Callable[[], None]] = None
        self.on_stop: Optional[Callable[[], None]] = None

    def _draw_rec(self) -> None:
        w, h = self.width, self.height
        w2 = self.small_circ_rad_proc * w
        h2 = self.small_circ_rad_proc * h
        self.create_oval(0, 0, w, h, fill="#aaaaac", outline="")
        self.create_oval(
            (w - w2) / 2,
            (h - h2) / 2,
            (w + w2) / 2,
            (h + h2) / 2,
            fill="#ff0000",
            outline="",
        )

        self.bind("<Button-1>", self._click_handler)

    def _click_handler(self, event: tk.Event) -> None:
        # distance from click to icon center
        midx = self.width / 2
        midy = self.height / 2
        r = self.width / 2

        dx = event.x - midx
        dy = event.y - midy
        dist_sq = dx**2 + dy**2
        if dist_sq <= r * r:  # inside the round button area
            self.toggle()

    def toggle(self) -> None:
        self.is_started = not self.is_started

        if self.is_started and self.on_start is not None:
            self.on_start()
        elif not self.is_started and self.on_stop is not None:
            self.on_stop()


class Timer(tk.Label):
    def __init__(self, master: tk.Widget, **kwargs: object):
        super().__init__(master, **kwargs)  # type: ignore[arg-type]

        self.start_time: float = 0
        self.running = False

    def start(self) -> None:
        self.start_time = time.time()
        self.running = True

        self.update()

    def stop(self) -> None:
        self.start_time = time.time()
        self.running = False

    def update(self) -> None:
        if not self.running:
            return

        elapsed = int(time.time() - self.start_time)
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60

        self.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        self.master.after(1000, self.update)


def add_coroutine(reactor: IReactorTime, coro: Callable[[], Coroutine]) -> None:
    reactor.callLater(0, lambda: defer.ensureDeferred(coro()))


class TkRecorder:
    def __init__(self, event_loop: IReactorTime, on_start: Callable[[], Coroutine], on_stop: Callable[[], Coroutine]):
        self.event_loop = event_loop
        self.on_start = on_start
        self.on_stop = on_stop

    def start(self) -> None:
        self.root = tk.Tk()
        self.root.title("Erpeto session")
        self.root.attributes("-topmost", True)

        self.frame = tk.Frame(self.root, padx=20, pady=20)
        self.frame.pack()

        self.rb = RecorderButton(self.frame)
        self.rb.pack(side=tk.LEFT, padx=10)

        font = tkfont.Font(family="Helvetica", size=25)
        self.timer = Timer(self.frame, text="00:00:00", font=font)
        self.timer.pack(side=tk.LEFT, padx=10)

        self.rb.on_start = self._on_start
        self.rb.on_stop = self._on_stop

        self.root.mainloop()

    def _on_start(self) -> None:
        self.timer.start()
        add_coroutine(self.event_loop, self.on_start)

    def _on_stop(self) -> None:
        self.timer.stop()
        add_coroutine(self.event_loop, self.on_stop)


class TkRecordControl(RecordControlUI):
    def __init__(self, event_loop: IReactorTime, on_start: Callable[[], Coroutine], on_stop: Callable[[], Coroutine]):
        tk_window = TkRecorder(event_loop, on_start, on_stop)
        self.tk_window = tk_window

        self.thread = threading.Thread(target=lambda: tk_window.start(), daemon=True)
        self.thread.start()
