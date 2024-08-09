import numpy as np


class PerlinNoiseManagement():
    def __init__(self):
        self.gradients = np.array([[1, 1], [-1, 1], [1, -1], [-1, -1],
                                   [1, 0], [-1, 0], [0, 1], [0, -1]])

        # Permutation table
        p = np.arange(256, dtype=int)
        np.random.seed(42)
        np.random.shuffle(p)
        self.p = np.stack([p, p]).flatten()

    def perlin(self, x, y, seed=0):
        np.random.seed(seed)

        # Determine grid cell coordinates
        xi = x.astype(int)
        yi = y.astype(int)

        # Internal coordinates
        xf = x - xi
        yf = y - yi

        # Fade factors
        u = self.fade(xf)
        v = self.fade(yf)

        # Hash coordinates of the 4 square corners
        n00 = self.hash_coords(xi, yi)
        n01 = self.hash_coords(xi, yi + 1)
        n11 = self.hash_coords(xi + 1, yi + 1)
        n10 = self.hash_coords(xi + 1, yi)

        # Gradient vectors
        g00 = self.gradients[n00 % 8]
        g01 = self.gradients[n01 % 8]
        g11 = self.gradients[n11 % 8]
        g10 = self.gradients[n10 % 8]

        # Noise contributions from each of the four corners
        x0 = xf
        y0 = yf
        x1 = xf - 1
        y1 = yf - 1
        n0 = self.dot_grid_gradient(g00, x0, y0)
        n1 = self.dot_grid_gradient(g10, x1, y0)
        ix0 = self.lerp(n0, n1, u)
        n0 = self.dot_grid_gradient(g01, x0, y1)
        n1 = self.dot_grid_gradient(g11, x1, y1)
        ix1 = self.lerp(n0, n1, u)

        return self.lerp(ix0, ix1, v)

    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, a, b, t):
        return a + t * (b - a)

    def dot_grid_gradient(self, grad, x, y):
        return grad[..., 0] * x + grad[..., 1] * y

    def hash_coords(self, x, y):
        return self.p[self.p[x % 256] + y % 256]

    def generate_perlin_noise_matrix(self, x_start, x_end, y_start, y_end, seed, scale=100.0):
        """
        Generates a matrix of Perlin noise values.

        Parameters:
            x_start (int): Starting coordinate in the x-axis.
            x_end (int): Ending coordinate in the x-axis.
            y_start (int): Starting coordinate in the y-axis.
            y_end (int): Ending coordinate in the y-axis.
            seed (int): Seed for the noise function.
            scale (float): Scale of the noise.

        Returns:
            np.ndarray: A matrix of Perlin noise values.
        """
        width = x_end - x_start
        height = y_end - y_start

        # Generate coordinate grid
        x = np.linspace(x_start, x_end, width, endpoint=False)
        y = np.linspace(y_start, y_end, height, endpoint=False)
        x, y = np.meshgrid(x / scale, y / scale)

        # Generate Perlin noise
        noise_matrix = self.perlin(x, y, seed)

        # Normalize the noise value to [0, 1]
        normalized_matrix = (noise_matrix + 1) / 2

        # print(normalized_matrix)
        return normalized_matrix
