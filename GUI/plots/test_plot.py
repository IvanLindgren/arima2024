import matplotlib.pyplot as plt
from random import randint


def plot() -> None:
    x = sorted([randint(-100, 100) for i in range(100)])
    y = sorted([randint(-100, 100) for i in range(100)])
    
    fig, ax = plt.subplots()
    fig.set_size_inches(10.5, 6.5)
    
    ax.plot(x, y)
    return fig

def save_plot(figure: plt.Figure, path: str, plot_name: str) -> None:
    fig = figure
    fig.savefig(f"{path}/{plot_name}")


 