# Modified from answers provided by Matt Gibson and Erotemic
# in https://stackoverflow.com/questions/4325733/save-a-subplot-in-matplotlib

from matplotlib.transforms import Bbox

def full_extent(ax, padx=0.0, pady=0.0,):
    """Get the full extent of an axes, including axes labels, tick labels, and
    titles."""
    # For text objects, we need to draw the figure first, otherwise the extents
    # are undefined.
    ax.figure.canvas.draw()
    items = ax.get_xticklabels() + ax.get_yticklabels() 
    items += [ax, ax.title, ax.get_xaxis().get_label(), ax.get_yaxis().get_label()]
    bbox = Bbox.union([item.get_window_extent() for item in items])

    return bbox.expanded(1.0 + padx, 1.0 + pady)