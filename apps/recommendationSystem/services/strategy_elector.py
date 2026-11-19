class StrategySelector:
    def __init__(self, strategies):
        self._strategies = sorted(
            strategies,
            key=lambda item: item[0],
            reverse=True
        )

    def select(self, history_size):
        for min_history, strategy in self._strategies:
            if history_size >= min_history:
                return strategy

        return None