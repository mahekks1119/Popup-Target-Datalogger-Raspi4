// Range Console — Stage 1 POC WebSocket client
// Connects to the Pi's WebSocket server, renders incoming dummy data,
// and sends motor rotation commands back to the Pi.

const connStatusEl = document.getElementById("connStatus");
const wsUrlInput = document.getElementById("wsUrl");
const connectBtn = document.getElementById("connectBtn");
const dataLogEl = document.getElementById("dataLog");
const motorButtons = document.querySelectorAll(".motor-btn");
const statusEls = {
  A: document.getElementById("statusA"),
  B: document.getElementById("statusB"),
};

let socket = null;

function setConnState(state) {
  // state: "connected" | "disconnected" | "connecting"
  connStatusEl.dataset.state = state;
  const label = connStatusEl.querySelector(".conn__label");
  label.textContent = state.toUpperCase();
}

function appendLogEntry(value, timestamp) {
  // Clear the placeholder message the first time real data arrives
  const placeholder = dataLogEl.querySelector(".log__empty");
  if (placeholder) placeholder.remove();

  const entry = document.createElement("div");
  entry.className = "log__entry";

  const time = document.createElement("span");
  time.className = "log__entry-time";
  time.textContent = new Date(timestamp).toLocaleTimeString();

  const val = document.createElement("span");
  val.className = "log__entry-value";
  val.textContent = value;

  entry.appendChild(time);
  entry.appendChild(val);
  dataLogEl.appendChild(entry);
  dataLogEl.scrollTop = dataLogEl.scrollHeight;
}

function handleServerMessage(raw) {
  let data;
  try {
    data = JSON.parse(raw);
  } catch (err) {
    console.warn("Received non-JSON message:", raw);
    return;
  }

  if (data.type === "dummy_data") {
    appendLogEntry(data.value, data.timestamp);
  } else if (data.type === "motor_ack") {
    const el = statusEls[data.motor];
    if (el) el.textContent = `${data.action} — ${data.status}`;
  } else {
    console.warn("Unknown message type:", data.type);
  }
}

function connect() {
  const url = wsUrlInput.value.trim();
  if (!url) return;

  setConnState("connecting");
  socket = new WebSocket(url);

  socket.addEventListener("open", () => {
    setConnState("connected");
  });

  socket.addEventListener("message", (event) => {
    handleServerMessage(event.data);
  });

  socket.addEventListener("close", () => {
    setConnState("disconnected");
    socket = null;
  });

  socket.addEventListener("error", () => {
    setConnState("disconnected");
  });
}

connectBtn.addEventListener("click", connect);

motorButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      alert("Not connected to the Pi yet.");
      return;
    }
    const motor = btn.dataset.motor;
    const action = btn.dataset.action;

    socket.send(JSON.stringify({
      type: "motor_command",
      motor,
      action,
    }));

    const el = statusEls[motor];
    if (el) el.textContent = `${action} — sending…`;
  });
});
