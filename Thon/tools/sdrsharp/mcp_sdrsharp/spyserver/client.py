"""SpyServer TCP protocol client.

Implements the SpyServer streaming protocol (version 2.0.1700) for remote
SDR access. Protocol verified from SDRSharp.dotnet8.exe binary analysis.

Protocol framing:
  Request:  [cmd_type: u32_le][param: u32_le][body...]
  Response: [msg_type_and_flags: u32_le][sequence: u32_le][body_size: u32_le][body...]

Constants extracted and verified via Kali Task K3 against the SDR# binary.
"""

import socket
import struct
import time
from dataclasses import dataclass, field

SPYSERVER_PROTOCOL_VERSION = 0x02000600  # 2.0.1700 in hex encoding
SPYSERVER_MAX_COMMAND_BODY_SIZE = 256
SPYSERVER_MAX_MESSAGE_BODY_SIZE = 1 << 20
SPYSERVER_MAX_DISPLAY_PIXELS = 1 << 15
SPYSERVER_MIN_DISPLAY_PIXELS = 100
SPYSERVER_MESSAGE_TYPE_BITS = 16

CMD_HELLO = 0
CMD_GET_SETTING = 1
CMD_SET_SETTING = 2
CMD_PING = 3

SETTING_STREAMING_MODE = 0
SETTING_STREAMING_ENABLED = 1
SETTING_GAIN = 2
SETTING_IQ_FREQUENCY = 101
SETTING_IQ_DECIMATION = 102
SETTING_IQ_DIGITAL_GAIN = 103
SETTING_IQ_FORMAT = 104
SETTING_FFT_FREQUENCY = 201
SETTING_FFT_DECIMATION = 202
SETTING_FFT_DB_OFFSET = 203
SETTING_FFT_DB_RANGE = 204
SETTING_FFT_DISPLAY_PIXELS = 205
SETTING_FFT_FORMAT = 206
SETTING_FFT_ZOOM = 207
SETTING_FFT_ZOOM_FREQUENCY = 208

STREAM_MODE_IQ_ONLY = 1
STREAM_MODE_AF_ONLY = 2
STREAM_MODE_FFT_ONLY = 4
STREAM_MODE_FFT_IQ = 5
STREAM_MODE_FFT_AF = 6

MSG_TYPE_DEVICE_INFO = 0
MSG_TYPE_CLIENT_SYNC = 1
MSG_TYPE_PONG = 2
MSG_TYPE_READ_SETTING = 3
MSG_TYPE_UINT8_IQ = 100
MSG_TYPE_INT16_IQ = 101
MSG_TYPE_INT24_IQ = 102
MSG_TYPE_FLOAT_IQ = 103
MSG_TYPE_UINT8_AF = 200
MSG_TYPE_INT16_AF = 201
MSG_TYPE_INT24_AF = 202
MSG_TYPE_FLOAT_AF = 203
MSG_TYPE_UINT8_FFT = 300
MSG_TYPE_UINT4_FFT = 301

HEADER_SIZE = 12  # 3 x u32


@dataclass
class SpyServerDeviceInfo:
    device_type: int = 0
    device_serial: int = 0
    max_sample_rate: int = 0
    max_bandwidth: int = 0
    decimation_stage_count: int = 0
    gain_stage_count: int = 0
    max_gain_index: int = 0
    min_frequency: int = 0
    max_frequency: int = 0
    resolution: int = 0
    min_iq_decimation: int = 0
    forced_iq_format: int = 0


@dataclass
class SpyServerClient:
    host: str = "127.0.0.1"
    port: int = 5555
    _sock: socket.socket | None = field(default=None, repr=False)
    _connected: bool = False
    _device_info: SpyServerDeviceInfo | None = None
    _sequence: int = 0

    def connect(self, timeout: float = 5.0) -> dict:
        """Connect to SpyServer and perform HELLO handshake."""
        if self._connected:
            return {"status": "already_connected", "host": self.host, "port": self.port}

        try:
            self._sock = socket.create_connection((self.host, self.port), timeout=timeout)
            self._sock.settimeout(timeout)
        except (OSError, ConnectionRefusedError, TimeoutError) as exc:
            return {
                "error": f"Cannot connect to SpyServer at {self.host}:{self.port}: {exc}",
                "troubleshooting": (
                    "Ensure SpyServer is running. Download from https://airspy.com/download/\n"
                    "Start with: spyserver --config=spyserver.config\n"
                    "Default port is 5555."
                ),
            }

        client_id = b"SDR-MCP"
        hello_body = struct.pack("<II", SPYSERVER_PROTOCOL_VERSION, len(client_id)) + client_id
        self._send_command(CMD_HELLO, 0, hello_body)

        response = self._read_response()
        if response is None:
            self.disconnect()
            return {"error": "No response to HELLO — server may not be a SpyServer instance"}

        self._connected = True

        if response["msg_type"] == MSG_TYPE_DEVICE_INFO and len(response["body"]) >= 40:
            self._parse_device_info(response["body"])

        return {
            "status": "connected",
            "host": self.host,
            "port": self.port,
            "device_info": self._format_device_info() if self._device_info else None,
        }

    def disconnect(self) -> dict:
        """Disconnect from SpyServer."""
        if self._sock:
            try:
                self._sock.close()
            except OSError:
                pass
            self._sock = None
        self._connected = False
        return {"status": "disconnected"}

    def set_frequency(self, freq_hz: int) -> dict:
        """Set the center frequency on the remote SDR."""
        if not self._connected:
            return {"error": "Not connected to SpyServer"}

        self._send_setting(SETTING_IQ_FREQUENCY, freq_hz)
        self._send_setting(SETTING_FFT_FREQUENCY, freq_hz)
        return {"status": "ok", "freq_hz": freq_hz}

    def set_gain(self, gain: int) -> dict:
        """Set RF gain on the remote SDR."""
        if not self._connected:
            return {"error": "Not connected to SpyServer"}

        self._send_setting(SETTING_GAIN, gain)
        return {"status": "ok", "gain": gain}

    def get_fft(self, pixels: int = 1024) -> dict:
        """Request FFT data from SpyServer.

        Returns an array of FFT magnitude bins.
        """
        if not self._connected:
            return {"error": "Not connected to SpyServer"}

        pixels = max(SPYSERVER_MIN_DISPLAY_PIXELS, min(pixels, SPYSERVER_MAX_DISPLAY_PIXELS))

        self._send_setting(SETTING_FFT_DISPLAY_PIXELS, pixels)
        self._send_setting(SETTING_STREAMING_MODE, STREAM_MODE_FFT_ONLY)
        self._send_setting(SETTING_STREAMING_ENABLED, 1)

        fft_data = None
        resp = None
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            resp = self._read_response(timeout=2.0)
            if resp is None:
                break
            if resp["msg_type"] in (MSG_TYPE_UINT8_FFT, MSG_TYPE_UINT4_FFT):
                fft_data = resp["body"]
                break

        self._send_setting(SETTING_STREAMING_ENABLED, 0)

        if fft_data is None:
            return {"error": "No FFT data received within timeout"}

        if resp["msg_type"] == MSG_TYPE_UINT8_FFT:
            bins = [float(b) - 128.0 for b in fft_data]
        else:
            bins = list(fft_data)

        return {
            "bins": bins,
            "bin_count": len(bins),
            "pixels": pixels,
            "format": "uint8" if resp["msg_type"] == MSG_TYPE_UINT8_FFT else "uint4",
        }

    def stream_iq(self, duration_sec: float = 1.0, output_file: str | None = None) -> dict:
        """Stream IQ data for a duration and save to file."""
        if not self._connected:
            return {"error": "Not connected to SpyServer"}

        from pathlib import Path
        from config import OUTPUT_DIR

        if not output_file:
            ts = time.strftime("%Y%m%d_%H%M%S")
            output_file = str(OUTPUT_DIR / f"spy_iq_{ts}.bin")

        out_path = Path(output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        self._send_setting(SETTING_STREAMING_MODE, STREAM_MODE_IQ_ONLY)
        self._send_setting(SETTING_STREAMING_ENABLED, 1)

        total_bytes = 0
        deadline = time.monotonic() + duration_sec
        with open(out_path, "wb") as f:
            while time.monotonic() < deadline:
                resp = self._read_response(timeout=1.0)
                if resp is None:
                    continue
                if resp["msg_type"] in (
                    MSG_TYPE_UINT8_IQ, MSG_TYPE_INT16_IQ,
                    MSG_TYPE_INT24_IQ, MSG_TYPE_FLOAT_IQ,
                ):
                    f.write(resp["body"])
                    total_bytes += len(resp["body"])

        self._send_setting(SETTING_STREAMING_ENABLED, 0)

        return {
            "file_path": str(out_path),
            "size_bytes": total_bytes,
            "duration_sec": duration_sec,
        }

    def ping(self) -> dict:
        """Ping the SpyServer to check connectivity."""
        if not self._connected:
            return {"error": "Not connected to SpyServer"}

        t0 = time.monotonic()
        self._send_command(CMD_PING, 0)
        resp = self._read_response(timeout=3.0)
        latency_ms = (time.monotonic() - t0) * 1000

        if resp and resp["msg_type"] == MSG_TYPE_PONG:
            return {"status": "pong", "latency_ms": round(latency_ms, 2)}
        return {"error": "No pong received", "latency_ms": round(latency_ms, 2)}

    def _send_command(self, cmd_type: int, param: int, body: bytes = b"") -> None:
        header = struct.pack("<II", cmd_type, param)
        self._sock.sendall(header + body)

    def _send_setting(self, setting_id: int, value: int) -> None:
        body = struct.pack("<I", value)
        self._send_command(CMD_SET_SETTING, setting_id, body)

    def _read_response(self, timeout: float = 5.0) -> dict | None:
        if not self._sock:
            return None
        self._sock.settimeout(timeout)
        try:
            header = self._recv_exact(HEADER_SIZE)
            if not header:
                return None
            msg_type_flags, sequence, body_size = struct.unpack("<III", header)
            msg_type = msg_type_flags & 0xFFFF
            body = self._recv_exact(body_size) if body_size > 0 else b""
            return {"msg_type": msg_type, "sequence": sequence, "body": body}
        except (socket.timeout, OSError):
            return None

    def _recv_exact(self, n: int) -> bytes:
        data = bytearray()
        while len(data) < n:
            chunk = self._sock.recv(n - len(data))
            if not chunk:
                return bytes(data)
            data.extend(chunk)
        return bytes(data)

    def _parse_device_info(self, body: bytes) -> None:
        if len(body) < 40:
            return
        fields = struct.unpack("<IIIIIIIIII", body[:40])
        self._device_info = SpyServerDeviceInfo(
            device_type=fields[0],
            device_serial=fields[1],
            max_sample_rate=fields[2],
            max_bandwidth=fields[3],
            decimation_stage_count=fields[4],
            gain_stage_count=fields[5],
            max_gain_index=fields[6],
            min_frequency=fields[7],
            max_frequency=fields[8],
            resolution=fields[9],
        )

    def _format_device_info(self) -> dict:
        if not self._device_info:
            return {}
        di = self._device_info
        device_names = {1: "Airspy One", 2: "Airspy HF+", 3: "RTL-SDR"}
        return {
            "device_type": device_names.get(di.device_type, f"Unknown ({di.device_type})"),
            "serial": di.device_serial,
            "max_sample_rate": di.max_sample_rate,
            "max_bandwidth": di.max_bandwidth,
            "gain_stages": di.gain_stage_count,
            "max_gain_index": di.max_gain_index,
            "freq_range_hz": f"{di.min_frequency}–{di.max_frequency}",
        }
