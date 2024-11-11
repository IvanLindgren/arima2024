import matplotlib.pyplot as plt
from random import randint


def plot():
    x = sorted([randint(-100, 100) for i in range(100)])
    y = sorted([randint(-100, 100) for i in range(100)])
    
    fig, ax = plt.subplots()
    fig.set_size_inches(5, 5)
    
    ax.plot(x, y)
    return fig

    