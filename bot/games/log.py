from collections.abc import Generator
from bot.games.report import Report


class Log:
    def __init__(self, size: int = 10):
        if not isinstance(size, int):
            raise TypeError(f'size precisa ser do tipo int ({type(size)}).')
        if size < 1:
            raise ValueError(f'size precisa ser maior que 0 ({size}).')

        self.logs = []
        self.size = size

    def __iter__(self) -> Generator[Report]:
        yield from reversed(self.logs)

    def __str__(self):
        log_text = ''
        for i, report in enumerate(self):
            i = len(self.logs) - i
            log_text += f'{i:02}: {report}\n'

        return log_text

    def add(self, report: Report):
        self.logs.append(report)
        if len(self.logs) > self.size:
            self.logs.pop(0)
