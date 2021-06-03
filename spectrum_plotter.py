import pandas as pd
from bokeh.embed.standalone import components
from bokeh.plotting import figure, output_file


def plot_bokeh_graph(spectrum):
    '''
    This function is used to plot an interactive graph using Bokeh
    Parameters:
        x: A pandas Series object for Wavelength
        y: A pandas Series object for Flux
    Returns:
        script: A string which can be placed into the HTML file directly as a part of the header scripts
        div: A string which represents a div element to be placed directly in the body of the HTML file
    '''
    # Output to a static HTML file
    output_file('lines.html')

    x, y = pd.Series(spectrum['wavelength']), pd.Series(spectrum['flux'])

    # Create a new plot with a title and axis labels
    plot = figure(title='Spectra', x_axis_label='Wavelength',
                    y_axis_label='Flux', plot_height=600, plot_width=680)

    # Add a line renderer with legend and line thickness
    plot.line(x, y, line_width=1)

    return plot

    # script, div = components(plot)

    # return script, div
