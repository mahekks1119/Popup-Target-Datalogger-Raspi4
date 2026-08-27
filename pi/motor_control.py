"""
Motor control stub — Stage 1 POC.

No actuators are wired up yet, so these functions just log what *would*
happen. Replace the function bodies with real gpiozero / RPi.GPIO calls once
the two motors controlling pop-up target rotation are physically connected.
"""

VALID_MOTORS = {"A", "B"}
VALID_ACTIONS = {"rotate_cw", "rotate_ccw", "stop"}


def rotate_motor_a(action: str) -> None:
    # TODO: replace with real gpiozero.Motor / PWM control for Motor A
    print(f"[motor_control] Motor A -> {action} (stub, no GPIO wired yet)")


def rotate_motor_b(action: str) -> None:
    # TODO: replace with real gpiozero.Motor / PWM control for Motor B
    print(f"[motor_control] Motor B -> {action} (stub, no GPIO wired yet)")


def handle_motor_command(motor: str, action: str) -> str:
    """
    Validate and dispatch a motor command coming in from the GUI.

    Returns a short status string ("ok" or an "error: ..." description)
    that server.py sends back to the GUI as an acknowledgement.
    """
    if motor not in VALID_MOTORS:
        print(f"[motor_control] Rejected: unknown motor {motor!r}")
        return f"error: unknown motor '{motor}'"

    if action not in VALID_ACTIONS:
        print(f"[motor_control] Rejected: unknown action {action!r}")
        return f"error: unknown action '{action}'"

    if motor == "A":
        rotate_motor_a(action)
    else:
        rotate_motor_b(action)

    return "ok"
