import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_football_field(linenumbers=True, endzones=True):
    rect = patches.Rectangle((0, 0), 120, 53.3, linewidth=0.1, edgecolor='r', facecolor='darkgreen', zorder=0)
    fig, ax = plt.subplots(1, figsize=(12.0, 6.33))
    ax.add_patch(rect)

    plt.plot([10, 10, 10, 20, 20, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80,
              80, 90, 90, 100, 100, 110, 110, 120, 0, 0, 120, 120],
             [0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3,
              53.3, 0, 0, 53.3, 53.3, 0, 0, 53.3, 53.3, 53.3, 0, 0, 53.3],
             color='white')
    # Endzones
    if endzones:
        ez1 = patches.Rectangle((0, 0), 10, 53.3,
                                linewidth=0.1, edgecolor='r', facecolor='blue', alpha=0.2, zorder=0)
        ez2 = patches.Rectangle((110, 0), 120, 53.3,
                                linewidth=0.1, edgecolor='r', facecolor='blue', alpha=0.2, zorder=0)
        ax.add_patch(ez1)
        ax.add_patch(ez2)
    plt.xlim(0, 120)
    plt.ylim(-5, 58.3)
    plt.axis('off')
    if linenumbers:
        for x in range(20, 110, 10):
                numb = x
                if x > 50:
                    numb = 120 - x
                plt.text(x, 5, str(numb - 10),
                         horizontalalignment='center',
                         fontsize=20, fontname='Arial', color='white')
                plt.text(x - 0.95, 53.3 - 5, str(numb - 10),
                         horizontalalignment='center',
                         fontsize=20, fontname='Arial', color='white', rotation=180)
    for x in range(11, 110):
        plt.plot([x, x], [0, 1], color='white')
        plt.plot([x, x], [53.3, 52.3], color='white')
        plt.plot([x, x], [18.5, 19.5], color='white')
        plt.plot([x, x], [34.8, 35.8], color='white')
    return fig, ax
