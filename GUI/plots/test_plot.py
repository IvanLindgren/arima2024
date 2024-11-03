import matplotlib.pyplot as plt
import numpy as np


def plot():
    data = np.random.rand(10, 10)

    fig, ax = plt.subplots()
    plt.figure(figsize=(5, 5))
    # Create a heatmap`your text`
    im = ax.imshow(data, cmap='hot', interpolation='nearest')
    fig.colorbar(im)  # Add a colorbar

    # Set axis labels
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # Set the title`your text`
    ax.set_title('Example of a heatmap')

    return fig