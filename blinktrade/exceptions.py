class OrderRejectedException(Exception):
    def __init__(self, message, details):
        self.message = message
        self.details = details
        super(OrderRejectedException, self).__init__(message)
