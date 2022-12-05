from sawtooth_sdk.processor.handler import TransactionHandler
from payload import BCPayload
from state import BCState
class BCTransactionHandler(TransactionHandler):
    def __init__(self, namespace_prefix):
        self._namespace_prefix = namespace_prefix

    @property
    def family_name(self):
        return 'bc'

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [self._namespace_prefix]

    def apply(self, transaction, context):
        header = transaction.header
        signer = header.signer_public_key

        payload = BCPayload.from_bytes(transaction.payload)

        state = BCState(context)

        if payload.action == 'delete':
            ...
        elif payload.action == 'create':
            ...
        elif payload.action == 'take':
            ...
