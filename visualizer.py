import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df=pd.read_csv('medical_examination.csv',)

# Add 'overweight' column
df['height']/=100
bmi=df['weight']/np.square(df['height'])
df['overweight'] = (bmi > 25).astype('uint8')

#If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['gluc']= (df['gluc']!=1).astype('uint8')
df['cholesterol']= (df['cholesterol']!=1).astype('uint8')

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat=pd.melt(df, id_vars='cardio', value_vars=
                  ['gluc','smoke','alco','alco','active','overweight'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.reset_index()

    df_cat=df_cat.groupby(['variable', 'cardio', 'value']).agg('count')

    df_cat =df_cat.rename(columns={'index':'Total'})
    

    # Draw the catplot with 'sns.catplot()'
    # Get the figure for the output
    fig = sns.catplot(df_cat, x='variable', y='Total', col='cardio', hue='value', kind='bar')

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat=df[(df['ap_lo']<=df['ap_hi']) &
               (df['height'] >= df['height'].quantile(0.025)) & 
               (df['height'] <= df['height'].quantile(0.975)) & 
               (df['weight'] >= df['weight'].quantile(0.025)) &
               (df['weight'] <= df['weight'].quantile(0.975))
          ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)]=True



    # Set up the matplotlib figure
    # Draw the heatmap with 'sns.heatmap()'
    fig=plt.figure(figsize=(12,4))
    sns.heatmap(corr,mask=mask)
    fig.savefig('heatmap.png')

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
