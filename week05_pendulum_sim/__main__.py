from __future__ import annotations

import argparse
from pathlib import Path

from .src import simulate_pendulum, save_simulation, plot_simulation


def main() -> None:
    parser = argparse.ArgumentParser(description="Single pendulum simulation")
    parser.add_argument("--length", type=float, default=1.0, help="Pendulum length in meters")
    parser.add_argument("--gravity", type=float, default=9.81, help="Gravitational acceleration")
    parser.add_argument("--theta0", type=float, default=1.5707963267948966, help="Initial angle in radians")
    parser.add_argument("--omega0", type=float, default=0.0, help="Initial angular velocity in rad/s")
    parser.add_argument("--damping", type=float, default=0.0, help="Linear damping coefficient")
    parser.add_argument("--dt", type=float, default=0.01, help="Time step in seconds")
    parser.add_argument("--total-time", type=float, default=10.0, help="Total simulation time in seconds")
    default_output = Path(__file__).resolve().parent / "results" / "pendulum.csv"
    parser.add_argument("--output", type=Path, default=default_output, help="CSV output path")
    parser.add_argument("--plot", action="store_true", help="Generate a plot image")
    args = parser.parse_args()

    result = simulate_pendulum(
        length=args.length,
        gravity=args.gravity,
        theta0=args.theta0,
        omega0=args.omega0,
        damping=args.damping,
        dt=args.dt,
        total_time=args.total_time,
    )

    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_simulation(result, output_path)

    if args.plot:
        plot_path = output_path.with_suffix(".png")
        plot_simulation(result, plot_path)
        print(f"Saved simulation to {output_path} and plot to {plot_path}")
    else:
        print(f"Saved simulation to {output_path}")


if __name__ == "__main__":
    main()
