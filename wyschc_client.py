"""Executes the sender-side of the project."""

from Entities.Rule import Rule
from Entities.SCHCSender import SCHCSender
from Entities.SigfoxProfile import SigfoxProfile
from utils.misc import generate_packet

# sizes = [11, 54, 96, 139, 181, 224, 266, 308]
sizes = [11]
# loss_rates = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
loss_rates = [90]

for size in sizes:

    PACKET = generate_packet(size)

    for repetition in range(10):
        for lr in loss_rates:
            print(f"PACKET SIZE = {size}")
            print(f"LOSS RATE = {lr}")
            print(f"(Repetition {repetition})")
            profile = SigfoxProfile("UPLINK", "ACK ON ERROR", Rule('000'))
            sender = SCHCSender(profile)

            sender.UPLINK_LOSS_RATE = lr
            sender.PROFILE.SIGFOX_DL_TIMEOUT = 1
            sender.PROFILE.RETRANSMISSION_TIMEOUT = 1
            sender.ENABLE_MAX_ACK_REQUESTS = False

            sender.start_session(PACKET)

            sender.LOGGER.export(
                f"size_{size}_"
                f"{str(lr).zfill(2)}_"
                f"rep{str(repetition).zfill(3)}"
            )

print("All experiments complete")
