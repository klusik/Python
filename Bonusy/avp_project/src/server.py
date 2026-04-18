"""Small RAW text print receiver.

Windows can forward Generic / Text Only printer jobs to a RAW TCP socket.
This module exposes a very small local listener that accepts such jobs and
passes the captured plain text to a callback.
"""

import socketserver
import threading


class _PrintRequestHandler(socketserver.BaseRequestHandler):
    """Receive all bytes from one print job connection."""

    def handle(self):
        """Read the full TCP stream and forward the decoded text payload."""
        received_chunks = []

        while True:
            received_data = self.request.recv(4096)
            if not received_data:
                break
            received_chunks.append(received_data)

        raw_payload = b"".join(received_chunks)
        decoded_text = raw_payload.decode("utf-8", errors="replace")
        self.server.on_text_received(decoded_text)


class _ThreadedPrintServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Threaded TCP server used by the local printer receiver."""

    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, server_address, request_handler_class, on_text_received):
        """Store callback and initialize the base TCP server."""
        self.on_text_received = on_text_received
        super().__init__(server_address, request_handler_class)


class PrintReceiverServer:
    """Manage the lifecycle of the local RAW printer receiver."""

    def __init__(self, host, port, on_text_received):
        """Prepare the server wrapper without starting it yet."""
        self.host = host
        self.port = port
        self.on_text_received = on_text_received
        self.server = None
        self.server_thread = None

    def start(self):
        """Start the TCP receiver in a background thread."""
        if self.server is not None:
            return

        self.server = _ThreadedPrintServer((self.host, self.port), _PrintRequestHandler, self.on_text_received)
        self.server_thread = threading.Thread(target=self.server.serve_forever, name="AVPPrintReceiver", daemon=True)
        self.server_thread.start()

    def stop(self):
        """Stop the TCP receiver and release the listening port."""
        if self.server is None:
            return

        self.server.shutdown()
        self.server.server_close()
        self.server = None
        self.server_thread = None
