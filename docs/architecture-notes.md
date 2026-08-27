# Architecture Notes

## WebSocket message format (Stage 1)

All messages are JSON text frames.

### Pi → GUI: dummy data

Sent whenever a line is typed at the Pi's SSH terminal.

```json
{
  "type": "dummy_data",
  "value": "whatever was typed",
  "timestamp": "2026-08-27T10:15:00.123456+00:00"
}
```

### GUI → Pi: motor command

Sent when a rotation button is clicked in the GUI.

```json
{
  "type": "motor_command",
  "motor": "A",
  "action": "rotate_cw"
}
```

- `motor`: `"A"` or `"B"`
- `action`: `"rotate_cw"` | `"rotate_ccw"` | `"stop"`

### Pi → GUI: motor acknowledgement

Sent back after the Pi processes a motor command (whether or not real
hardware is attached).

```json
{
  "type": "motor_ack",
  "motor": "A",
  "action": "rotate_cw",
  "status": "ok",
  "timestamp": "2026-08-27T10:15:01.000000+00:00"
}
```

`status` is `"ok"` or an `"error: ..."` string if the motor/action was
invalid.

## Open decisions (not yet designed)

- **Bullet-hit location recording** — what sensor(s) detect a hit, how
  location on the target is calculated, and how it's represented in the
  data model. Deliberately not designed yet; `dummy_data.value` is a
  free-form string for now so this can slot in later without changing the
  transport layer.
- **Target rotation mechanics** — exact motor hardware (stepper vs DC),
  gearing, and whether rotation is by angle or continuous CW/CCW/stop.
  Current `motor_command` schema assumes CW/CCW/stop; will likely need an
  `angle` or `speed` field once hardware is chosen.
- **Access point vs. shared WiFi** — POC currently assumes Pi and laptop
  share the "ms" WiFi network per the setup log. Falling back to Pi-as-AP
  for isolated field testing is mentioned in the tech stack plan but not
  yet configured.

## Staged plan (for reference — see Wireless_Protocol_Tech_Stack_Plan doc for full detail)

1. **POC on laptop (browser)** — this repo, current state.
2. **POC on tablet (browser)** — zero code changes, same GUI opened on tablet.
3. **Installed app on laptop** — Electron or PWA wrapping the same GUI.
4. **Installed app on tablet** — Capacitor or PWA wrapping the same GUI.
5. **Multi-device MQTT logging** — additive on the Pi side only (`paho-mqtt`
   client per Pi → Mosquitto broker on a central logger), doesn't touch the
   WebSocket/GUI code above.
