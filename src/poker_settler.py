import copy
from dataclasses import dataclass, field
from threading import Lock


class PokerSettler:
    @dataclass
    class Result:
        name: str
        buyin: int
        cashout: int
        diff: int = None

        def __post_init__(self):
            if not self.diff:
                self.diff = self.cashout - self.buyin

        def __str__(self):
            return f"{self.name} IN: {self.buyin} OUT: {self.cashout} DIFF: {self.diff}"

    @dataclass
    class Transfer:
        src: str
        dst: str
        amount: int

        def __str__(self):
            return f"{self.src} -> {self.dst}: {self.amount}"

    @dataclass
    class Settlement:
        transfers: []
        unmatched: []

        def __bool__(self):
            return bool(self.transfers)

        def __str__(self):
            transfers_str = '\n'.join([str(transfer) for transfer in self.transfers])
            unmatched_str = '\n'.join([str(unmatch) for unmatch in self.unmatched])
            if self.transfers and not self.unmatched:
                return f"Settled:\n{transfers_str}"
            elif not self.transfers and self.unmatched:
                return f"Cannot settle! Unmatched results:\n{unmatched_str}"
            elif self.transfers and self.unmatched:
                return f"Unexpected state! Transfers and unmatched are not empty!\n" \
                       f"Transfers:\n{transfers_str}\n" \
                       f"Unmatched:\n{unmatched_str}"
            else:
                return "Empty settlement"

        def reset(self):
            self.transfers = []
            self.unmatched = []

    _results: [Result]
    _settlement: Settlement

    def __init__(self):
        self._lock = Lock()
        self._results = []
        self._settlement = PokerSettler.Settlement([], [])

    def reset(self) -> None:
        self.__init__()

    def add_result(self, name: str, buyin: int, cashout: int) -> None:
        with self._lock:
            self._results.append(self.Result(name, buyin, cashout))

    def settlement(self) -> str:
        with self._lock:
            self._settlement.reset()
            winners, losers = self._split_winners_and_losers()
            winners, losers = self._settle_exact_matches(winners, losers)
            winners, losers = self._settle_all(winners, losers)
            if winners or losers:
                self._settlement.unmatched.extend(winners)
                self._settlement.unmatched.extend(losers)
            return str(self._settlement)

    @property
    def results(self):
        return self._results

    def _split_winners_and_losers(self) -> ([Result], [Result]):
        winners = []
        losers = []
        for result in self._results:
            if result.buyin < result.cashout:
                winners.append(copy.deepcopy(result))
            elif result.buyin > result.cashout:
                losers.append(copy.deepcopy(result))
        return winners, losers

    def _settle_exact_matches(self, winners: [Result], losers: [Result]) -> ([Result], [Result]):
        for loser in losers:
            for winner in winners:
                if loser.diff + winner.diff == 0:
                    self._settlement.transfers.append(self.Transfer(loser.name, winner.name, winner.diff))
                    loser.diff = 0
                    winner.diff = 0
        return [winner for winner in winners if winner.diff], [loser for loser in losers if loser.diff]

    def _settle_all(self, winners, losers) -> ([Result], [Result]):
        for loser in losers:
            for winner in winners:
                if winner.diff > 0:
                    transfer_amount = min(abs(loser.diff), abs(winner.diff))
                    self._settlement.transfers.append(
                        self.Transfer(loser.name, winner.name, transfer_amount))
                    loser.diff += transfer_amount
                    winner.diff -= transfer_amount
                    if loser.diff == 0:
                        break
        return [winner for winner in winners if winner.diff], [loser for loser in losers if loser.diff]
