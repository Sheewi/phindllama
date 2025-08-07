# transaction_router.py
class TransactionRouter:
    def __init__(self):
        self.layers = [
            TimeDecoyLayer(),
            AmountSplittingLayer(),
            ChainHoppingLayer(),
            CounterpartyRotation()
        ]
    
    def route(self, tx):
        for layer in self.layers:
            tx = layer.apply(tx)
        return tx