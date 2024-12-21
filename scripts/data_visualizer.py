import seaborn as sns
import matplotlib.pyplot as plt


def visualize_bivariate(plot_type,df,x_axis, y_axis):
    """
    plot bivariate graph 
    Args:
        plot_type: Type of plot to draw
        df: data frame
        x_axis: the first variable on the x axis
        y_axis: the sceond variable on the y axis
    """
    if(plot_type == 'lineplot'):
        sns.lineplot(data=df, x=x_axis, y=y_axis, palette = 'viridis')
    elif(plot_type == 'scatterplot'):
        sns.scatterplot(df, x=x_axis, y=y_axis, color='blue')
    else:
        sns.barplot(df, x=x_axis, y=y_axis, color='blue')

    plt.figure(figsize=(12, 6))
    plt.title( x_axis + "vs." + y_axis)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    #plt.xticks(rotation=45)  # Rotate x-axis labels if needed
    plt.tight_layout()
    plt.show()
    


 



def visualize_univariate(plot_type,df,x_axis):
    """
    plot univariate graph 
    Args:
        plot_type: Type of plot to draw
        df: data frame
        x_axis: the first variable on the x axis
        
    """
    plt.figure(figsize=(10, 6))
    if(plot_type == 'histplot'):
        sns.histplot(x_axis, bins=30, kde=True)
    elif(plot_type == 'barplot'):
        sns.histplot(x_axis, bins=30, kde=True)
    else:
        sns.histplot(x_axis, bins=30, kde=True)

    
    #plt.title( )
    plt.xlabel(x_axis)
    plt.ylabel('Frequency')
    plt.show()