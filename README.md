# Popup-Target-Datalogger-Raspi4
Data logging system for popup target training ranges, using a Raspberry Pi 4B for full-duplex Wi-Fi transmission of hit/timing data

# Raspberry Pi Target Range — Stage 1 POC

Wireless communication POC between a Raspberry Pi 4 and a laptop/tablet
browser, over a WebSocket. This is the foundation stage: everything later
(tablet browser, installed apps, MQTT multi-device logging) builds on this
code unchanged. See `docs/architecture-notes.md` for the full staged plan
and open decisions.

## What this does right now

- The Pi runs a Python WebSocket server (`pi/server.py`).
- Typing a line into the Pi's SSH terminal broadcasts it as dummy data to
  any connected browser GUI — a stand-in for real bullet-hit sensor data,
  which is still to be decided.
- The GUI (`gui/index.html`) shows that incoming data live, and has two
  motor controls (CW / CCW / stop) that send rotation commands back to the
  Pi. No actuators are wired up yet, so the Pi just logs what it would do
  (`pi/motor_control.py`).

## Repo layout

```
pi/
  server.py          WebSocket server + terminal-input loop
  motor_control.py   Motor command stubs (no GPIO wired yet)
  requirements.txt   Pi-side Python dependencies
gui/
  index.html         GUI page
  style.css
  app.js             WebSocket client logic
docs/
  architecture-notes.md   Message format, open decisions, stage plan
```

## Running it

**On the Pi** (over SSH, inside the existing `gpio-env` venv):

```bash
source ~/gpio-env/bin/activate
pip3 install -r pi/requirements.txt   # websockets, in addition to what's already installed
python3 pi/server.py
```

You should see:

```
[server] Starting WebSocket server on ws://0.0.0.0:8765
Enter dummy data >
```

**On the laptop:**

- Open `gui/index.html` directly in a browser (Chrome/Edge/Firefox), or serve it from the Pi later.
- Make sure the laptop is on the same WiFi network as the Pi (SSID `ms`).
- In the "Pi address" field, confirm it reads `ws://msraspi4.local:8765`, then click **Connect**.

Type anything at the Pi's `Enter dummy data >` prompt and press Enter — it
should appear in the GUI's data log immediately. Click a motor button in
the GUI — the Pi terminal should print a stub log line for that motor.

## Next stages (not yet implemented)

See `docs/architecture-notes.md` and the tech stack plan doc for Stage
2–5 (tablet browser, Electron/PWA laptop app, Capacitor/PWA tablet app,
MQTT multi-device logging). None of the code above needs to be rewritten
for those — only added to.