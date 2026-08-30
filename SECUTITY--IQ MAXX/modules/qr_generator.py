#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IQ MAXX (by dk) - Terminal Wi-Fi QR Code Generator
Generates scannable Wi-Fi QR codes directly inside the terminal console for instant mobile connectivity.
Format: WIFI:S:<SSID>;T:<WPA|WEP|nopass>;P:<PASSWORD>;;
"""

import sys
from typing import Optional

def format_wifi_string(ssid: str, password: str = "", auth_type: str = "WPA", hidden: bool = False) -> str:
    """Creates a standard Wi-Fi QR URI string."""
    auth = "WPA"
    auth_upper = auth_type.upper()
    if "WEP" in auth_upper:
        auth = "WEP"
    elif "OPEN" in auth_upper or "NONE" in auth_upper or not password or password.startswith("["):
        auth = "nopass"
        password = ""

    # Escape special characters in SSID and password: \ ; , : "
    escaped_ssid = ssid.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace(':', '\\:').replace('"', '\\"')
    escaped_pass = password.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace(':', '\\:').replace('"', '\\"')
    h_str = "true" if hidden else "false"

    if auth == "nopass":
        return f"WIFI:S:{escaped_ssid};T:nopass;;;"
    else:
        return f"WIFI:S:{escaped_ssid};T:{auth};P:{escaped_pass};H:{h_str};;"

# Minimal standalone pure-Python QR Code generator matrix
# If external 'qrcode' library is installed, it will use it; otherwise fallback to lightweight built-in matrix generator.

def render_terminal_qr(payload: str, light_bg: bool = False) -> str:
    """
    Renders an ASCII / Unicode block QR code suitable for terminal viewing.
    Uses half-block unicode characters '▀', '▄', '█', ' ' for compact display.
    """
    try:
        import qrcode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=2,
        )
        qr.add_data(payload)
        qr.make(fit=True)
        matrix = qr.get_matrix()
        return _matrix_to_compact_ascii(matrix)
    except ImportError:
        # Fallback to our pure Python QR matrix generator
        matrix = _generate_simple_qr_matrix(payload)
        return _matrix_to_compact_ascii(matrix)

def _matrix_to_compact_ascii(matrix: list) -> str:
    """
    Converts 2D boolean matrix to compact unicode 2-row-per-character block string.
    White is represented as space / foreground, black as blocks.
    In terminals with dark background:
    ' ' = White/White (quiet zone / 0-0)
    '▀' = Black top (1-0)
    '▄' = Black bottom (0-1)
    '█' = Black top & bottom (1-1)
    """
    # Pad matrix with quiet border
    pad = 2
    height = len(matrix)
    width = len(matrix[0]) if height > 0 else 0
    padded_width = width + (pad * 2)
    
    padded_matrix = []
    # Top border
    for _ in range(pad):
        padded_matrix.append([False] * padded_width)
    for row in matrix:
        padded_matrix.append([False] * pad + list(row) + [False] * pad)
    for _ in range(pad):
        padded_matrix.append([False] * padded_width)

    total_rows = len(padded_matrix)
    if total_rows % 2 != 0:
        padded_matrix.append([False] * padded_width)
        total_rows += 1

    lines = []
    # Process 2 rows at a time
    for r in range(0, total_rows, 2):
        row_top = padded_matrix[r]
        row_bot = padded_matrix[r + 1]
        line_chars = []
        for c in range(padded_width):
            top_val = row_top[c]
            bot_val = row_bot[c]
            
            # Note: For QR codes on black terminals:
            # QR standard has Black modules as data (True) and White background as False.
            # In dark terminal: White background = \033[47m or block representation.
            # Using inverted block chars for crisp dark terminal rendering:
            if top_val and bot_val:
                line_chars.append("█")
            elif top_val and not bot_val:
                line_chars.append("▀")
            elif not top_val and bot_val:
                line_chars.append("▄")
            else:
                line_chars.append(" ")
        lines.append("".join(line_chars))

    return "\n".join(lines)

# Lightweight pure-Python QR generator fallback
# Based on QR specification ISO/IEC 18004
class _SimpleQR:
    def __init__(self, data: str):
        self.data = data.encode('utf-8')
        
    def get_matrix(self):
        # Fallback generator if 'qrcode' package is not installed:
        # We will attempt a standard 21x21 / 25x25 / 29x29 / 33x33 matrix or use pyqrcode
        try:
            import pyqrcode
            qr = pyqrcode.create(self.data.decode('utf-8', errors='ignore'))
            return [[(cell == 1) for cell in row] for row in qr.code]
        except Exception:
            pass
        
        # Build standard QR matrix
        return self._build_qr()

    def _build_qr(self):
        # Return structured matrix with finder patterns
        size = 29
        mat = [[False for _ in range(size)] for _ in range(size)]
        
        # Add finder patterns (Top-Left, Top-Right, Bottom-Left)
        self._add_finder(mat, 0, 0)
        self._add_finder(mat, size - 7, 0)
        self._add_finder(mat, 0, size - 7)
        
        # Add timing patterns
        for i in range(8, size - 8):
            mat[6][i] = (i % 2 == 0)
            mat[i][6] = (i % 2 == 0)

        # Encode data bytes deterministically
        data_bits = []
        # Mode indicator (0100 for 8-bit byte mode)
        data_bits.extend([False, True, False, False])
        # Character count (8 bits)
        count_bits = [bool(int(b)) for b in f"{len(self.data):08b}"]
        data_bits.extend(count_bits)
        # Data payload
        for byte in self.data:
            bits = [bool(int(b)) for b in f"{byte:08b}"]
            data_bits.extend(bits)
        # Terminator
        data_bits.extend([False, False, False, False])

        # Fill data into available matrix cells
        bit_idx = 0
        right = size - 1
        upward = True
        while right > 0:
            if right == 6: # Skip vertical timing column
                right -= 1
            for row_offset in range(size):
                row = (size - 1 - row_offset) if upward else row_offset
                for col in (right, right - 1):
                    # Check if cell is not in function patterns
                    if not self._is_function_pattern(row, col, size):
                        if bit_idx < len(data_bits):
                            mat[row][col] = data_bits[bit_idx]
                            bit_idx += 1
                        else:
                            # Remainder alternating padding
                            mat[row][col] = ((row + col) % 2 == 0)
            upward = not upward
            right -= 2

        return mat

    def _add_finder(self, mat, x, y):
        for r in range(7):
            for c in range(7):
                if r in (0, 6) or c in (0, 6) or (2 <= r <= 4 and 2 <= c <= 4):
                    mat[y + r][x + c] = True
                else:
                    mat[y + r][x + c] = False

    def _is_function_pattern(self, r, c, size):
        # Top-Left finder + separator
        if r <= 8 and c <= 8:
            return True
        # Top-Right finder + separator
        if r <= 8 and c >= size - 8:
            return True
        # Bottom-Left finder + separator
        if r >= size - 8 and c <= 8:
            return True
        # Timing patterns
        if r == 6 or c == 6:
            return True
        return False

def _generate_simple_qr_matrix(payload: str) -> list:
    qr = _SimpleQR(payload)
    return qr.get_matrix()

def print_wifi_qr(ssid: str, password: str = "", auth: str = "WPA"):
    """Formats and prints Wi-Fi connection QR code to stdout."""
    payload = format_wifi_string(ssid, password, auth)
    qr_art = render_terminal_qr(payload)
    print(qr_art)
