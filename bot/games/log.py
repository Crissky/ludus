from bot.games.report import Report


class Log:
    def __init__(self, size: int = 10):
        self.logs = []
        self.size = size

    def __iter__(self):
        yield from (report for report in reversed(self.logs))

    def __str__(self):
        log_text = ''
        for i, report in enumerate(self, start=1):
            log_text += f'{i}: {report}\n'

        return log_text

    def add(self, report: Report):
        self.logs.append(report)
        if len(self.logs) > self.size:
            self.logs.pop(0)
