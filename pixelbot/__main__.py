"""Entry point for `pixelbot` / `python -m pixelbot`."""

from __future__ import annotations

import argparse
import sys

from .launcher import run


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="pixelbot",
        description="Pixel Bot — desktop automation for Path of Exile and similar games.",
    )
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Run the backend only. Open http://localhost:<port> in any browser.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Preferred port (a free port near it will be chosen if taken).",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable Flask debug mode (verbose logs, auto-reload).",
    )
    args = parser.parse_args()

    sys.exit(run(no_gui=args.no_gui, port=args.port, debug=args.debug) or 0)


if __name__ == "__main__":
    main()
