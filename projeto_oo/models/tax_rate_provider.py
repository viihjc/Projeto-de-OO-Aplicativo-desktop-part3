class TaxRateProvider:
    """Fornece as taxas de rendimento aplicáveis."""
    def __init__(self, savings_rate=0.005):
        self.savings_rate = savings_rate

    def calcular_rendimento(self, saldo_inicial, meses):
        """Calcula o rendimento composto da poupança."""
        return saldo_inicial * ((1 + self.savings_rate) ** meses - 1)