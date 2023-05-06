from Entities.exceptions import LengthMismatchError
from config.schc import L2_WORD_SIZE, UPLINK_MTU_BITS
from utils.casting import bin_to_int, hex_to_bin, int_to_bin
from utils.misc import round_to_next_multiple, is_monochar


class Rule:

    def __init__(self, rule_id_binary: str) -> None:

        if rule_id_binary[:3] != '111':
            id_int = bin_to_int(rule_id_binary)
            rule_id_size = 3
            t = 0
            m = 2
            n = 3
            window_size = 7
            u = 3
            max_packet_size = 300

        elif rule_id_binary[:6] != '111111':
            id_int = (bin_to_int(rule_id_binary) & 7) + 6
            rule_id_size = 6
            t = 0
            m = 2
            n = 4
            window_size = 12
            u = 4
            max_packet_size = 480

        else:
            id_int = (bin_to_int(rule_id_binary) & 3) + 15
            rule_id_size = 8
            t = 0
            m = 3
            n = 5
            window_size = 31
            u = 5
            max_packet_size = 2400

        if len(rule_id_binary) > rule_id_size:
            raise LengthMismatchError("Rule ID is larger than RULE_ID_SIZE")

        header_length: int = round_to_next_multiple(
            rule_id_size + t + m + n, L2_WORD_SIZE
        )

        all1_header_length: int = round_to_next_multiple(
            rule_id_size + t + m + n + u, L2_WORD_SIZE
        )

        ack_header_length: int = rule_id_size + m + 1

        max_window_number = 2 ** m
        max_fragment_number = max_window_number \
                              * window_size

        self.FCN_DICT = {
            int_to_bin(
                window_size - (j % window_size) - 1, n
            ): j
            for j in range(window_size)
        }

        regular_payload_length = UPLINK_MTU_BITS - header_length
        max_all1_payload_length = UPLINK_MTU_BITS - all1_header_length

        self.FRG_INDICES = {
            "rule_id_idx": 0,
            "dtag_idx": rule_id_size,
            "w_idx": rule_id_size + t,
            "fcn_idx": rule_id_size + t + m,
            "rcs_idx": rule_id_size + t + m + n
        }

        self.ACK_INDICES = {
            "rule_id_idx": 0,
            "dtag_idx": rule_id_size,
            "w_idx": rule_id_size + t,
            "c_idx": rule_id_size + t + m,
            "bitmap_idx": rule_id_size + t + m + 1,
            "tuple_idx": rule_id_size + t + m + 1 + window_size
        }

        self.BIN = rule_id_binary
        self.ID = id_int
        self.RULE_ID_SIZE = rule_id_size
        self.T = t
        self.M = m
        self.N = n
        self.U = u
        self.WINDOW_SIZE = window_size
        self.HEADER_LENGTH = header_length
        self.ALL1_HEADER_LENGTH = all1_header_length
        self.ACK_HEADER_LENGTH = ack_header_length
        self.MAX_WINDOW_NUMBER = max_window_number
        self.MAX_FRAGMENT_NUMBER = max_fragment_number
        self.REGULAR_PAYLOAD_LENGTH = regular_payload_length
        self.MAX_ALL1_PAYLOAD_LENGTH = max_all1_payload_length
        self.MAX_PACKET_SIZE = max_packet_size

    @staticmethod
    def from_hex(hexa: str) -> 'Rule':
        """Parses the Rule ID of the given hex string,
         assuming that it is located in the leftmost bits."""
        as_bin = hex_to_bin(hexa)
        first_byte = as_bin[:8]
        rule_id = first_byte[:3]
        if is_monochar(rule_id, '1'):
            rule_id = first_byte[:6]
            if is_monochar(rule_id, '1'):
                rule_id = first_byte[:8]
        return Rule(rule_id)
