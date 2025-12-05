"""
Manim Community Edition (manimce) script
Class: TemperatureEvolution

Features:
- Accepts a NumPy array `temp_matrix` of shape (T, N) where rows are time steps and
  columns are positions (N = 101, positions in x span from 0 to 2 by default).
- Shows an evolving 2D line plot (x vs temperature) where the current curve
  smoothly transforms into the next curve (no left-to-right drawing).
- Keeps past curves visible with reduced opacity.
- At the end, moves every curve along the z-axis so you can view the full
  evolution in 3D (z = time index * dz). `dz` is a configurable variable.
- Uses the Plasma colormap for line coloring and a dark background.

How to use:
- Replace the example `temp_matrix` generation with your NumPy array (same name).
  Or load: temp_matrix = np.load("/path/to/your/data.npy")
- Run with manim (adjust flags as needed):
    manim -pqh manim_temperature_evolution.py TemperatureEvolution

Adjustable params are at the top of the script.
"""

import os

import manim as mm
import numpy as np
from matplotlib import cm


def carregar_posicions_temperatures(fitxer):
    output_dir = os.path.join(os.getcwd(), "dades")
    full_filepath = os.path.join(output_dir, fitxer + ".csv")

    if not os.path.exists(full_filepath):
        print(f"Error: El fitxer '{full_filepath}' no existeix.")
        return np.array([], dtype=object), np.array([], dtype=np.float64)

    # Llegim la 1a línia, amb les posicions en l'eix x
    try:
        with open(full_filepath, "r") as f:
            # Treiem tots els caracters espai, salts de línia i tabulacions
            header_line = f.readline().strip()

            header_elements = header_line.split(",")

            processed_header = []
            # Convertim tots els valors a np.float64 (sempre que es pugui)
            for item in header_elements:
                try:
                    processed_header.append(np.float64(item))
                except ValueError:
                    print(" Error al processar els headers, tractats com strings ")
                    processed_header.append(item)

            header_array = np.array(processed_header, dtype=object)

    except Exception as e:
        print(f" Error al llegir els headers: {e}")
        return np.array([], dtype=object), np.array([], dtype=np.float64)

    # Llegim la matriu de temperatures (les files són les iteracions temporals)
    try:
        data_matrix = np.loadtxt(
            full_filepath, dtype=np.float64, delimiter=",", skiprows=1
        )

    except Exception as e:
        print(f" Error al llegir la matriu: {e}")
        return header_array, np.array([], dtype=np.float64)

    return header_array, data_matrix

# -------------------------- USER-CONFIGURABLE PARAMETERS --------------------------
# If you already have a NumPy array, set temp_matrix = your_array (shape: T x N)
# Example synthetic data is created below if you don't replace it.

# Spatial domain
X_MIN = 0.0
X_MAX = 2.0
N_COLS = 101  # number of spatial points (columns)

# Z spacing per time-step when building the 3D stack
DZ = 0.05  # <--- change this as you like

# Interpolation time between successive time-steps (seconds)
INTERP_TIME = 1/15  # <--- ~0.02 as requested

# Stroke / style
STROKE_WIDTH = 1.0  # thin lines (increase for thicker)
BASE_OPACITY = 0.6  # opacity of the immediately previous curve
MIN_OPACITY = 0.08  # lower bound so very old lines stay faintly visible
OPACITY_DECAY = 0.85  # multiplicative decay per age step

# Colormap name (matplotlib)
COLORMAP = cm.get_cmap("viridis_r")

# Example data generation (replace with your data)
# temp_matrix should have shape (T, N_COLS) where T between 101 and 300
T = 160  # number of time-steps (rows); replace or load your own data
x_values = np.linspace(X_MIN, X_MAX, N_COLS)
# Simple travelling wave + diffusion-ish pattern as placeholder
x,temp_matrix = carregar_posicions_temperatures("implicit_1")
# temp_matrix = np.array([
#     np.sin(np.pi * x_values * (1 + 0.5 * np.sin(2 * np.pi * t / T))) *
#     np.exp(-0.5 * ((x_values - (1.0 + 0.5 * np.sin(2 * np.pi * t / T))) ** 2) * 2.0)
#     for t in range(T)
# ])
# ---------------------------------------------------------------------------------


def rgba_to_color(rgba):
    """Convert matplotlib RGBA (0..1) to manim Color."""
    r, g, b, a = rgba
    return mm.rgb_to_color((r, g, b))


def make_curve_from_xy(x, y, z=0.0):
    """Return a VMobject representing a smooth polyline through (x[i], y[i], z)."""
    pts = [np.array([float(xi), float(yi), float(z)]) for xi, yi in zip(x, y)]
    curve = mm.VMobject()
    # set_points_smoothly expects a list of points; it will create a smooth path
    curve.set_points_smoothly(pts)
    return curve


class TemperatureEvolution(mm.ThreeDScene):
    def construct(self):
        # Scene params
        t_steps, n_cols = temp_matrix.shape
        assert n_cols == N_COLS, f"Expected {N_COLS} columns, got {n_cols}"

        # Dark background and axes setup
        self.camera.background_color = mm.DARKER_GRAY

        axes = mm.Axes(
            x_range=[X_MIN, X_MAX, (X_MAX - X_MIN) / 4],
            y_range=[float(np.min(temp_matrix)) - 0.1, float(np.max(temp_matrix)) + 0.1,
                     (np.max(temp_matrix) - np.min(temp_matrix)) / 4 if np.max(temp_matrix) != np.min(temp_matrix) else 1],
            x_length=10,
            y_length=5,
            tips=False,
        )
        axes.to_edge(mm.LEFT)

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("Temperature")
        title = mm.Title("Temperature evolution (x vs Temperature)")

        # Add axes and labels
        self.add(axes, x_label, y_label, title)

        # Precompute color for each time-step using colormap
        colors = [rgba_to_color(COLORMAP(i / max(1, t_steps - 1))) for i in range(t_steps)]

        # Map data-space -> axes coordinates
        x_coords = list(x_values)

        # Create initial curve (time 0)
        current_curve = make_curve_from_xy(x_coords, temp_matrix[0], z=0.0)
        current_curve.set_stroke(colors[0], width=STROKE_WIDTH)
        current_curve.set_opacity(1.0)
        # Put the curve in the scene coordinates by mapping its points through the axes
        current_curve.apply_function(lambda p: axes.coords_to_point(p[0], p[1]))
        # Since apply_function maps z as well, ensure z remains 0 in manim scene units
        # (we'll manage z shifts later when moving to 3D)

        self.add(current_curve)

        # Keep track of previous frozen curves (for z-shifting at the end)
        frozen_curves = []

        # Loop through time-steps, morphing current curve -> next curve each time
        for k in range(1, t_steps):
            next_curve = make_curve_from_xy(x_coords, temp_matrix[k], z=0.0)
            next_curve.set_stroke(colors[k], width=STROKE_WIDTH)
            next_curve.set_opacity(1.0)
            next_curve.apply_function(lambda p: axes.coords_to_point(p[0], p[1]))

            # Create a frozen copy of the current curve to remain on screen with reduced opacity
            frozen_copy = current_curve.copy()
            # Reduce opacity according to age (newer frozen ones are more opaque)
            # We linearly decay using OPACITY_DECAY and clamp with MIN_OPACITY
            age = 0  # for this freshly frozen curve
            frozen_opacity = max(MIN_OPACITY, BASE_OPACITY * (OPACITY_DECAY ** len(frozen_curves)))
            frozen_copy.set_opacity(frozen_opacity)
            frozen_copy.set_stroke(width=STROKE_WIDTH)
            frozen_curves.append(frozen_copy)

            # Add frozen copy beneath the transforming curve so it sits behind
            self.add(frozen_copy)

            # Transform current_curve smoothly into next_curve
            # We use Transform which will interpolate points
            self.play(mm.Transform(current_curve, next_curve), run_time=INTERP_TIME, rate_func=mm.linear)

            # After transform, current_curve now matches next_curve - continue loop

        # At this point we've shown the full evolution in 2D with historical curves visible
        # Now we create the 3D stacked structure by moving each frozen curve and the final
        # current_curve to distinct z positions so the z-axis encodes time.

        # Prepare animations to shift each curve along +z (so time grows into the screen)
        all_curves = frozen_curves + [current_curve]
        animations = []
        for i, c in enumerate(all_curves):
            # Move each curve so its z-position becomes i * DZ
            # Since curves were placed using axes.coords_to_point, their points currently
            # have z=0. We shift by a vector along the scene z-axis.
            shift_vec = np.array([0, 0, i * DZ])
            animations.append(c.animate.shift(shift_vec))

            # Optionally, make older curves slightly dimmer when turned into 3D
            new_opacity = max(MIN_OPACITY, c.get_fill_opacity() * 0.9)
            animations.append(c.set_fill_opacity(new_opacity))

        print(type(animations[0]))#,type(animations[0].animation))
        print(*animations)
        # Play the z-stack animation with a bit of stagger (lag) for nicer effect
        self.play(mm.LaggedStart(*[ani for ani in animations], lag_ratio=0.02), run_time=2.0)

        # Keep the final structure on screen
        self.wait(2)

        # That's it. Camera movement/orbiting is left to the user per your request.


# End of file
