import hashlib

from sawtooth_sdk.processor.exceptions import InternalError


BC_NAMESPACE = hashlib.sha512('bc'.encode("utf-8")).hexdigest()[0:6]


def _make_bc_address(vin):
    return BC_NAMESPACE + \
        hashlib.sha512(vin.encode('utf-8')).hexdigest()[:64]


class VehicleHisotry:
    def __init__(self, vin, vehicle_info, events):
        self.vin = vin
        self.events = events


class BCState:

    TIMEOUT = 3

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to
                validator state from within the transaction processor.
        """

        self._context = context
        self._address_cache = {}

    def set_vin(self, vin, vehicle):
        """Store the game in the validator state.
        Args:
            game_name (str): The name.
            game (Game): The information specifying the current game.
        """

        vehicle = self._load_vehicle(vin=vin)

        #vehicle[vin] = game

        self._store_vehicle(vin, vehicle=vehicle)

    def get_vehicle(self, vin):
        """Get the vehicle associated with vin.
        Args:
            vin (str): The name.
        Returns:
            (Vehicle): All the information specifying a vehicle.
        """

        return self._load_vehicle(vin=vin)

    def _store_vehicle(self, vin, vehicle):
        address = _make_bc_address(vin)

        state_data = self._serialize(vehicle)

        self._address_cache[address] = state_data

        self._context.set_state(
            {address: state_data},
            timeout=self.TIMEOUT)

    # def _delete_game(self, game_name):
    #     address = _make_xo_address(game_name)

    #     self._context.delete_state(
    #         [address],
    #         timeout=self.TIMEOUT)

    #     self._address_cache[address] = None

    def _load_vehicle(self, vin):
        address = _make_bc_address(vin)

        if address in self._address_cache:
            if self._address_cache[address]:
                serialized_vehicle = self._address_cache[address]
                vehicle = self._deserialize(serialized_vehicle)
            else:
                vehicle = ""
        else:
            state_entries = self._context.get_state(
                [address],
                timeout=self.TIMEOUT)
            if state_entries:

                self._address_cache[address] = state_entries[0].data

                vehicle = self._deserialize(data=state_entries[0].data)

            else:
                self._address_cache[address] = None
                vehicle = ""

        return vehicle

    def _deserialize(self, data):
        """Take bytes stored in state and deserialize them into Python
        Vehicle objects.
        Args:
            data (bytes): The UTF-8 encoded string stored in state.
        Returns:
            (dict): game name (str) keys, Game values.
        """

        vehicle = {}
        try:
            for v in data.decode().split("|"):
                vin, make, model, events = v.split(",")

                vehicle[vin] = Vehicle(vin, make, model, events)
        except ValueError as e:
            raise InternalError("Failed to deserialize game data") from e

        return vehicle

    def _serialize(self, vehicle):
        """Takes a vehicle and serializes it
        Args:
            vehicle (Vehicle)
        Returns:
            (bytes): The UTF-8 encoded string stored in state.
        """
        vehicle_str = ",".join(
            [vehicle.vin, vehicle.make, vehicle.model, vehicle.events])

        return vehicle_str.encode()