FR_MODE = "ACK ON ERROR"
RETRANSMISSION_TIMEOUT = 100  # in seconds
SIGFOX_DL_TIMEOUT = 60  # in seconds
INACTIVITY_TIMEOUT = 500  # in seconds
MAX_ACK_REQUESTS = 5
L2_WORD_SIZE = 8
DELAY_BETWEEN_FRAGMENTS = 10

# Sender config
ENABLE_MAX_ACK_REQUESTS = False

# Receiver config
RESET_DATA_AFTER_REASSEMBLY = True
CHECK_FOR_CALLBACK_RETRIES = False
DISABLE_INACTIVITY_TIMEOUT = True

RECEIVER_URL = "http://localhost:5000/receive"
REASSEMBLER_URL = "http://localhost:5000/reassemble"
