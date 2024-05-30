import asyncio
import time

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService
from iot.helpers import run_parallel, run_sequence


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()

    created_devices = await asyncio.gather(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    hue_light_id, speaker_id, toilet_id = created_devices

    sequence_programs = [
        service.run_program(Message(speaker_id, MessageType.SWITCH_ON)),
        service.run_program(Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")),
    ]
    parallel_programs = [
        service.run_program(Message(hue_light_id, MessageType.SWITCH_ON)),
        run_sequence(*sequence_programs)
    ]

    await run_parallel(*parallel_programs)

    sequence_programs = [
        service.run_program(Message(toilet_id, MessageType.FLUSH)),
        service.run_program(Message(toilet_id, MessageType.CLEAN)),
    ]
    parallel_programs = [
        service.run_program(Message(hue_light_id, MessageType.SWITCH_OFF)),
        service.run_program(Message(speaker_id, MessageType.SWITCH_OFF)),
        run_sequence(*sequence_programs)
    ]
    await run_parallel(*parallel_programs)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
