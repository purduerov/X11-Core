"""Simple example showing how to get gamepad events."""

from inputs import get_gamepad
import signal
import json
import sys

def interrupt_handler(bttn, axis, fileout="gp_params.json"):
    def signal_handler(sig, frame):
        print("Ctrl+C sensed!")

        with open(fileout, "w") as fp:
            fp.write(json.dumps({"bttn": bttn, "axis": axis}, indent=4, sort_keys=True))

        print("File written, closing")
        sys.exit(0)
    
    return signal_handler

def main():
    """Just print out some event infomation when the gamepad is used."""
    bttn = {}
    axis = {}

    # signal.signal(signal.SIGINT, interrupt_handler(bttn, axis))

    while 1:
        events = get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)

            if event.ev_type == "Absolute":
                if event.code not in axis:
                    axis[event.code] = {"val": 0, "max": 0, "min": 0}
                
                axis[event.code]["val"] = event.state
                
                if event.state > axis[event.code]["max"]:
                    axis[event.code]["max"] = event.state
                
                if event.state < axis[event.code]["min"]:
                    axis[event.code]["min"] = event.state

            elif event.ev_type == "Key":
                if event.code not in bttn:
                    bttn[event.code] = {"val": 0, "max": 0, "min": 0}
                
                bttn[event.code]["val"] = event.state
                
                if event.state > bttn[event.code]["max"]:
                    bttn[event.code]["max"] = event.state
                
                if event.state < bttn[event.code]["min"]:
                    bttn[event.code]["min"] = event.state


if __name__ == "__main__":
    main()