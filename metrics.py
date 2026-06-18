from abc import ABC, abstractmethod

import psutil


class Metric(ABC):
    def __init__(self, name):
        self._name = name
        self._value = 0

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def get_info(self):
        ...

    def get_percent(self):
        return self._value


class CPUMetric(Metric):
    def __init__(self):
        super().__init__("CPU")
        self._freq = 0

    def update(self):
        self._value = psutil.cpu_percent(interval=0.1)
        freq = psutil.cpu_freq()
        if freq:
            self._freq = freq.current

    def get_info(self):
        return f"{self._value:.1f}%   |   {self._freq:.0f} МГц"


class RAMMetric(Metric):
    def __init__(self):
        super().__init__("RAM")
        self._used_gb = 0
        self._total_gb = 0

    def update(self):
        mem = psutil.virtual_memory()
        self._value = mem.percent
        self._used_gb = mem.used / (1024 ** 3)
        self._total_gb = mem.total / (1024 ** 3)

    def get_info(self):
        return f"{self._used_gb:.1f} / {self._total_gb:.1f} ГБ  ({self._value:.1f}%)"


class DiskMetric(Metric):
    def __init__(self, path="C:\\"):
        super().__init__("Диск")
        self._path = path
        self._used_gb = 0
        self._total_gb = 0

    def update(self):
        try:
            disk = psutil.disk_usage(self._path)
            self._value = disk.percent
            self._used_gb = disk.used / (1024 ** 3)
            self._total_gb = disk.total / (1024 ** 3)
        except OSError:
            self._value = 0

    def get_info(self):
        return f"{self._used_gb:.1f} / {self._total_gb:.1f} ГБ  ({self._value:.1f}%)"


class NetworkMetric(Metric):
    def __init__(self):
        super().__init__("Сеть")
        self._sent_mb = 0
        self._recv_mb = 0

    def update(self):
        net = psutil.net_io_counters()
        self._sent_mb = net.bytes_sent / (1024 ** 2)
        self._recv_mb = net.bytes_recv / (1024 ** 2)

    def get_info(self):
        return f"Отправлено: {self._sent_mb:.1f} МБ     Получено: {self._recv_mb:.1f} МБ"
