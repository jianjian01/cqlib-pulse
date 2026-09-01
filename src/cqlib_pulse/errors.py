# (C) Copyright China Telecom Quantum Group 2026

"""Public exceptions raised by :mod:`cqlib_pulse`."""


class PulseError(Exception):
    """Base exception for this package."""


class PulseValidationError(PulseError, ValueError):
    """A pulse target or parameter is invalid."""


class QCISParseError(PulseError, ValueError):
    """A QCIS source line cannot be parsed as a supported pulse command."""


class TianyanIntegrationError(PulseError, RuntimeError):
    """The optional Tianyan integration is missing or incompatible."""


class WaveformAPIError(PulseError, RuntimeError):
    """The cloud waveform API request or response is invalid."""


class TianyanAuthenticationError(WaveformAPIError):
    """An API Key cannot be exchanged for a Tianyan access token."""
