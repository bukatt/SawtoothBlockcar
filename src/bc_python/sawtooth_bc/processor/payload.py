from sawtooth_sdk.processor.exceptions import InvalidTransaction

class BCPayload:

    def __init__(self, payload):
        try:
            # The payload is csv utf-8 encoded string
            provider, action, vehicle = payload.decode().split(",")
        except ValueError as e:
            raise InvalidTransaction("Invalid payload serialization") from e

        if not provider:
            raise InvalidTransaction('Provider is required')

        if not action:
            raise InvalidTransaction('Action is required')

        if not vehicle:
            raise InvalidTransaction('Target vehicle is required')

        if action not in ('oil change', 'tire rotation', 'accident'):
            raise InvalidTransaction('Invalid action: {}'.format(action))

        self._provider = provider
        self._action = action
        self._vehicle = vehicle

    @staticmethod
    def from_bytes(payload):
        return BCPayload(payload=payload)

    @property
    def provider(self):
        return self._provider

    @property
    def action(self):
        return self._action

    @property
    def vehicle(self):
        return self._vehicle