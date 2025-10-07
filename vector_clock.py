# vector_clock.py
from typing import Dict

class VectorClock:
    def __init__(self, pid: str = None, clock: Dict[str,int] = None):
        self.pid = pid
        self.clock = dict(clock) if clock else {}

    def increment(self, pid: str = None):
        pid = pid or self.pid
        if pid is None:
            raise ValueError("pid required for increment")
        self.clock[pid] = self.clock.get(pid, 0) + 1
        return self.clock

    def merge(self, other: Dict[str,int]):
        for k, v in (other or {}).items():
            self.clock[k] = max(self.clock.get(k, 0), v)

    def to_dict(self) -> Dict[str,int]:
        return dict(self.clock)

    @staticmethod
    def compare(a: Dict[str,int], b: Dict[str,int]) -> str:
        less = False
        greater = False
        keys = set(a.keys()) | set(b.keys())
        for k in keys:
            av = a.get(k, 0)
            bv = b.get(k, 0)
            if av < bv:
                less = True
            elif av > bv:
                greater = True
        if less and not greater:
            return 'less'
        if greater and not less:
            return 'greater'
        if not less and not greater:
            return 'equal'
        return 'concurrent'

    def __repr__(self):
        return f"VectorClock(pid={self.pid}, clock={self.clock})"
