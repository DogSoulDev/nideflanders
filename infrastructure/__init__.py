"""Infrastructure adapters package."""
from .tor_controller import TorController  # type: ignore
from .privoxy_controller import PrivoxyController  # type: ignore

__all__ = ["TorController", "PrivoxyController"]
