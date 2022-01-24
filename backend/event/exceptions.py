class PaymentIncompleteException(Exception):
    def __init__(self,  registration):
        super().__init__("Payment incomplete.")
        self.registration = registration
