import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Simulation function with realistic shuttle drag
# -----------------------------
def simulate_trajectory(v0_kmh, theta_deg, y0=0.6, x0=0):
    # Shuttlecock parameters
    m = 0.005       # kg
    Cd = 0.5        # higher drag for shuttle
    A = 0.003       # cross-sectional area (m^2)
    rho = 1.225     # air density (kg/m^3)
    g = 9.81        # gravity (m/s^2)
    n = 2         # drag exponent
    k = 0.5 * Cd * rho * A

    dt = 0.01
    t_max = 5       # shorter simulation time
    N = int(t_max / dt)

    # Initial velocities
    theta_rad = np.radians(theta_deg)
    vx0 = v0_kmh / 3.6 * np.cos(theta_rad)
    vy0 = v0_kmh / 3.6 * np.sin(theta_rad)

    # Arrays
    x = np.zeros(N)
    y = np.zeros(N)
    vx = np.zeros(N)
    vy = np.zeros(N)

    # Initial conditions
    x[0], y[0] = x0, y0
    vx[0], vy[0] = vx0, vy0

    # Simulation loop
    for i in range(N - 1):
        v = np.sqrt(vx[i]**2 + vy[i]**2)
        F_drag = k * v**n
        ax = -(F_drag / m) * vx[i] / v
        ay = -g - (F_drag / m) * vy[i] / v

        # Update velocities and positions
        vx[i+1] = vx[i] + ax * dt
        vy[i+1] = vy[i] + ay * dt
        x[i+1] = x[i] + vx[i] * dt
        y[i+1] = y[i] + vy[i] * dt

        if y[i+1] <= 0 and i > 0:  # stop when shuttle hits ground
            x = x[:i+2]
            y = y[:i+2]
            break

    return x, y

# -----------------------------
# Plotting function for multiple compact vertical trajectories
# -----------------------------
def plot_multiple_trajectories_vertical(trajectories, title="Badminton Clears Comparison"):
    n = len(trajectories)
    fig, axes = plt.subplots(n, 1, figsize=(6, 2*n))  # compact height

    if n == 1:
        axes = [axes]

    for ax, (v0, theta, y0, x0) in zip(axes, trajectories):
        x, y = simulate_trajectory(v0, theta, y0, x0)
        label_str = f"v0={v0} km/h, θ={theta}°, x0={x0} m"
        ax.plot(x, y, label=label_str, color='blue')
        ax.set_xlabel("Horizontal distance (m)", fontsize=9)
        ax.set_ylabel("Height (m)", fontsize=9)
        ax.set_title(label_str, fontsize=10)
        ax.grid(True, linewidth=0.5)
        ax.tick_params(axis='both', labelsize=8)
        ax.legend(fontsize=8)
        ax.set_xticks([0, 0.76, 4.67, 6.705, 8.685, 12.65, 13.41])
        ax.set_xticklabels(["|","|","|","|","|","|","|"], fontsize=8)

    plt.suptitle(title, fontsize=12)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# -----------------------------
# Example usage with multiple trajectories
# -----------------------------
trajectory_params = [
    (200, 45, 0.6, 0),
    (100, 55, 0.6, 4.67),
    (117, 60, 0.6, 4.67),
    (147, 60, 0.6, 4.67),
    (170, 65, 0.6, 4.67),
    (200, 65, 0.6, 4.67),
        (220, 65, 0.6, 4.67)
]

plot_multiple_trajectories_vertical(trajectory_params, title="Badminton Clears Comparison")
## so the conclusion is to lift powerfully at a bigger angle. due to the drag, the high lift will likely to land in. For example,at 65%, the initial speed from (170 to 220 km/h) will land in back corner. whereas at 60 degree, the range is (117 - 145km/hr)