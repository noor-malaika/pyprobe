"""Shared logger for the entire `pyprobe` package.

All modules should use this logger so logs are consistently named and configured.
"""

import logging

logger = logging.getLogger("pyprobe")
