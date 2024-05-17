import plotly.express as px
from bokeh.plotting import figure, output_file, save
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Plotly Visualizations
def plot_scatter_plotly(df, x_col, y_col):
    """
    Create a scatter plot using Plotly.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - x_col (str): The name of the column to use for the x-axis.
    - y_col (str): The name of the column to use for the y-axis.
    """
    fig = px.scatter(df, x=x_col, y=y_col, title="Scatter Plot")
    fig.show()

def plot_line_plotly(df, x_col, y_col):
    """
    Create a line plot using Plotly.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - x_col (str): The name of the column to use for the x-axis.
    - y_col (str): The name of the column to use for the y-axis.
    """
    fig = px.line(df, x=x_col, y=y_col, title="Line Plot")
    fig.show()

def plot_histogram_plotly(df, col):
    """
    Create a histogram using Plotly.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - col (str): The name of the column to use for the histogram.
    """
    fig = px.histogram(df, x=col, title="Histogram")
    fig.show()

def plot_bar_plotly(df, x_col, y_col):
    """
    Create a bar plot using Plotly.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - x_col (str): The name of the column to use for the x-axis.
    - y_col (str): The name of the column to use for the y-axis.
    """
    fig = px.bar(df, x=x_col, y=y_col, title="Bar Plot")
    fig.show()

def plot_box_plotly(df, col):
    """
    Create a box plot using Plotly.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - col (str): The name of the column to use for the box plot.
    """
    fig = px.box(df, y=col, title="Box Plot")
    fig.show()

def plot_heatmap_plotly(df, cols):
    """
    Create a heatmap using Plotly.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - cols (list): The columns to use for the heatmap.
    """
    corr_matrix = df[cols].corr()
    fig = px.imshow(corr_matrix, text_auto=True, title="Heatmap")
    fig.show()

# Bokeh Visualizations
def plot_scatter_bokeh(df, x_col, y_col, output_filename="scatter.html"):
    """
    Create a scatter plot using Bokeh and save it as an HTML file.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - x_col (str): The name of the column to use for the x-axis.
    - y_col (str): The name of the column to use for the y-axis.
    - output_filename (str): The name of the output HTML file.
    """
    p = figure(title="Scatter Plot", x_axis_label=x_col, y_axis_label=y_col)
    p.scatter(df[x_col], df[y_col])
    output_file(output_filename)
    save(p)

def plot_line_bokeh(df, x_col, y_col, output_filename="line.html"):
    """
    Create a line plot using Bokeh and save it as an HTML file.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - x_col (str): The name of the column to use for the x-axis.
    - y_col (str): The name of the column to use for the y-axis.
    - output_filename (str): The name of the output HTML file.
    """
    p = figure(title="Line Plot", x_axis_label=x_col, y_axis_label=y_col)
    p.line(df[x_col], df[y_col], line_width=2)
    output_file(output_filename)
    save(p)

def plot_histogram_bokeh(df, col, output_filename="histogram.html"):
    """
    Create a histogram using Bokeh and save it as an HTML file.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - col (str): The name of the column to use for the histogram.
    - output_filename (str): The name of the output HTML file.
    """
    p = figure(title="Histogram", x_axis_label=col, y_axis_label='Frequency')
    hist, edges = np.histogram(df[col], bins=50)
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:])
    output_file(output_filename)
    save(p)

def plot_bar_bokeh(df, x_col, y_col, output_filename="bar.html"):
    """
    Create a bar plot using Bokeh and save it as an HTML file.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - x_col (str): The name of the column to use for the x-axis.
    - y_col (str): The name of the column to use for the y-axis.
    - output_filename (str): The name of the output HTML file.
    """
    p = figure(title="Bar Plot", x_axis_label=x_col, y_axis_label=y_col)
    p.vbar(x=df[x_col], top=df[y_col], width=0.9)
    output_file(output_filename)
    save(p)

def plot_box_bokeh(df, col, output_filename="box.html"):
    """
    Create a box plot using Bokeh and save it as an HTML file.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - col (str): The name of the column to use for the box plot.
    - output_filename (str): The name of the output HTML file.
    """
    p = figure(title="Box Plot", y_axis_label=col)
    p.boxplot(df[col])
    output_file(output_filename)
    save(p)

def plot_heatmap_bokeh(df, cols, output_filename="heatmap.html"):
    """
    Create a heatmap using Bokeh and save it as an HTML file.

    Parameters:
    - df (pd.DataFrame): The data frame containing the data to plot.
    - cols (list): The columns to use for the heatmap.
    - output_filename (str): The name of the output HTML file.
    """
    corr_matrix = df[cols].corr()
    p = figure(title="Heatmap")
    heatmap = sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.savefig(output_filename)
    plt.close()