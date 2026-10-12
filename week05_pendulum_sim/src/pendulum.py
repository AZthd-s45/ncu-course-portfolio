from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover - optional dependency
    plt = None


@dataclass(frozen=True)
class PendulumParameters:
    length: float = 1.0
    gravity: float = 9.81
    damping: float = 0.0


class SimulationResult(list):
    def __init__(self, times: Sequence[float], angles: Sequence[float], velocities: Sequence[float], **metadata):
        super().__init__([(float(t), float(theta), float(omega)) for t, theta, omega in zip(times, angles, velocities)])
        self.time = list(map(float, times))
        self.theta = list(map(float, angles))
        self.omega = list(map(float, velocities))
        self.metadata = dict(metadata)

    def as_dict(self):
        return {
            "time": list(self.time),
            "theta": list(self.theta),
            "omega": list(self.omega),
            **self.metadata,
        }


class Pendulum:
    def __init__(self, length: float = 1.0, gravity: float = 9.81, damping: float = 0.0, theta0: float = 0.0, omega0: float = 0.0):
        if length <= 0:
            raise ValueError("Pendulum length must be positive.")
        if gravity <= 0:
            raise ValueError("Gravity must be positive.")
        self.length = float(length)
        self.gravity = float(gravity)
        self.damping = float(damping)
        self.theta = float(theta0)
        self.omega = float(omega0)

    @property
    def parameters(self) -> PendulumParameters:
        return PendulumParameters(length=self.length, gravity=self.gravity, damping=self.damping)

    def angular_acceleration(self, theta: float, omega: float) -> float:
        return -(self.gravity / self.length) * math.sin(theta) - self.damping * omega

    def _euler_step(self, theta: float, omega: float, dt: float) -> tuple[float, float]:
        alpha = self.angular_acceleration(theta, omega)
        theta_next = theta + omega * dt
        omega_next = omega + alpha * dt
        return theta_next, omega_next

    def _rk4_step(self, theta: float, omega: float, dt: float) -> tuple[float, float]:
        def derivative(th: float, om: float):
            return om, self.angular_acceleration(th, om)

        k1_t, k1_o = derivative(theta, omega)
        k2_t, k2_o = derivative(theta + 0.5 * dt * k1_t, omega + 0.5 * dt * k1_o)
        k3_t, k3_o = derivative(theta + 0.5 * dt * k2_t, omega + 0.5 * dt * k2_o)
        k4_t, k4_o = derivative(theta + dt * k3_t, omega + dt * k3_o)

        theta_next = theta + (dt / 6.0) * (k1_t + 2 * k2_t + 2 * k3_t + k4_t)
        omega_next = omega + (dt / 6.0) * (k1_o + 2 * k2_o + 2 * k3_o + k4_o)
        return theta_next, omega_next

    def step(self, dt: float, method: str = "rk4") -> tuple[float, float]:
        method_name = method.lower()
        if method_name in {"rk4", "runge-kutta", "runge_kutta", "fourth-order"}:
            self.theta, self.omega = self._rk4_step(self.theta, self.omega, dt)
        elif method_name in {"euler", "forward-euler", "explicit-euler"}:
            self.theta, self.omega = self._euler_step(self.theta, self.omega, dt)
        else:
            raise ValueError(f"Unsupported numerical method: {method!r}")
        return self.theta, self.omega

    def simulate(self, dt: float = 0.01, total_time: float = 10.0, method: str = "rk4") -> SimulationResult:
        if dt <= 0:
            raise ValueError("Time step dt must be positive.")
        if total_time < 0:
            raise ValueError("Total simulation time must be non-negative.")

        times = [0.0]
        angles = [self.theta]
        velocities = [self.omega]

        step_count = int(total_time / dt)
        for _ in range(step_count):
            self.step(dt=dt, method=method)
            times.append(times[-1] + dt)
            angles.append(self.theta)
            velocities.append(self.omega)

        return SimulationResult(
            times,
            angles,
            velocities,
            length=self.length,
            gravity=self.gravity,
            damping=self.damping,
            method=method,
            total_time=total_time,
            dt=dt,
        )


def simulate_pendulum(
    length: float = 1.0,
    gravity: float = 9.81,
    theta0: float = 0.0,
    omega0: float = 0.0,
    damping: float = 0.0,
    dt: float = 0.01,
    total_time: float = 10.0,
    method: str = "rk4",
) -> SimulationResult:
    """Simulate a simple nonlinear pendulum using RK4 by default."""
    pendulum = Pendulum(length=length, gravity=gravity, damping=damping, theta0=theta0, omega0=omega0)
    return pendulum.simulate(dt=dt, total_time=total_time, method=method)


def save_simulation(result: Iterable, output_path: str | Path) -> Path:
    file_path = Path(output_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    records = list(result)
    if not records:
        raise ValueError("Simulation result is empty.")

    fieldnames = ["time", "theta", "omega"]
    with file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for time_value, theta_value, omega_value in records:
            writer.writerow({"time": time_value, "theta": theta_value, "omega": omega_value})
    return file_path


def plot_simulation(result: Iterable, output_path: str | Path = "results/pendulum.png") -> Path:
    if plt is None:
        raise RuntimeError("matplotlib is required to create plot output.")

    records = list(result)
    if not records:
        raise ValueError("Simulation result is empty.")

    times = [row[0] for row in records]
    angles = [row[1] for row in records]

    fig, axis = plt.subplots(figsize=(8, 5))
    axis.plot(times, angles, label="theta(t)", linewidth=2)
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Angle (rad)")
    axis.set_title("Simple Pendulum Simulation")
    axis.grid(True, alpha=0.3)
    axis.legend()
    fig.tight_layout()

    file_path = Path(output_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(file_path)
    plt.close(fig)
    return file_path


def run_simulation(**kwargs):
    return simulate_pendulum(**kwargs)


simulate = simulate_pendulum
run = run_simulation
save_results = save_simulation
plot_results = plot_simulation
SinglePendulum = Pendulum
PendulumSimulation = SimulationResult
