from sawtooth_sdk.processor.core import TransactionProcessor
from handler import BCTransactionHandler

def main():
    # In docker, the url would be the validator's container name with
    # port 4004
    processor = TransactionProcessor(url='tcp://localhost:4004')

    handler = BCTransactionHandler()

    processor.add_handler(handler)

    processor.start()