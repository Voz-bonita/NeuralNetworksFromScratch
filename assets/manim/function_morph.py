from manim import *
import numpy as np
import numpy as np
import matplotlib.cm as cm


class ColoredSurface(MovingCameraScene):
    def construct(self):
        self.camera.background_color = "#191919"
        self.renderer.camera.frame_rate = 60
        self.renderer.pixel_height = 1080
        self.renderer.pixel_width = 1920
        self.play(self.camera.frame.animate.set(width=20))
        self.play(self.camera.frame.animate.move_to(UP))

        axes = Axes(
            x_range=[-5, 5],
            y_range=[-5, 25],
            axis_config={"color": WHITE},
        )

        identity_func = axes.plot(lambda x: x, color=BLUE)
        square_func = axes.plot(lambda x: x**2 - 5, color=GREEN)

        label1 = MathTex("f(x) = x", color=BLUE).move_to(axes.c2p((0, 4, 0))[0])
        label2 = MathTex("f(x) = x^2 - 3", color=GREEN).move_to(axes.c2p((0, 4, 0))[0])
        label3 = MathTex(
            "f(x_1) = x_1 x_2 + x_1^2 + e^{\sin(x_2)}", color=PURPLE
        ).move_to(axes.c2p((0, 4, 0))[0])

        self.add(axes, identity_func, label1)
        self.wait(2)
        self.play(Transform(identity_func, square_func), Transform(label1, label2))
        self.wait(2)

        # Define function
        def func(x, y):
            return x * y + x**2 + np.exp(np.sin(y))

        # Generate grid points
        x_vals = np.linspace(-3, 3, 30)
        y_vals = np.linspace(-3, 3, 30)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = func(X, Y)
        min_Z, max_Z = np.min(Z), np.max(Z)
        points = []
        dots = []
        for x in x_vals:
            for y in y_vals:
                dot = Dot(
                    point=axes.c2p([x, y, 0])[0],
                    color=self.get_color(
                        self.normalize_value(func(x, y), min_Z, max_Z)
                    ),
                    radius=0.2,
                )
                dots.append(dot)
                points.append((x, y, 0))
        points = np.array(points)
        points_group = VGroup(*dots)
        self.play(Transform(identity_func, points_group), Transform(label1, label3))
        self.wait(2)

    @staticmethod
    def normalize_value(value, minimum, maximum):
        return (value - minimum) / (maximum - minimum)

    def get_color(self, value):
        """Function to map function values to viridis colors."""
        cmap = cm.get_cmap("viridis")
        rgba = cmap(value)
        return rgb_to_color(rgba[:3])
