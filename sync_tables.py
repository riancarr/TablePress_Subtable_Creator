import pandas as pd
import regex as re
import os


#read in main file
all_themes_df = pd.read_csv('45-All-Themes-Set-Ranking-2023-10-02.csv')
brickset_sets_df = pd.read_csv('Brickset-Sets.csv')

#remove the '-1' of the set number to match the formatting of my tables
brickset_sets_df['Number'] = brickset_sets_df['Number'].str.rstrip('-1')
brickset_sets_df.to_csv('Brickset-Sets.csv', index=False)

#further divide themes into subtables
def divide_into_subtables(theme, theme_group):

    if theme == 'LEGO Creator Expert':
        #divide into modulars and vehicles
    elif theme == 'LEGO Star Wars':
        #divide into helmets, dioramas, ucs and playsets


#group by theme
theme_groups = all_themes_df.groupby('THEME')

for theme, theme_group in theme_groups:
    if '<a href' in theme:
        sanatized_theme_name = re.search(r'>([^<]+)</a>', theme)
        print(sanatized_theme_name.group(1))
        if sanatized_theme_name.group(1) == 'LEGO Star Wars' or sanatized_theme_name.group(1) == 'LEGO Creator Expert':
            divide_into_subtables(sanatized_theme_name.group(1), theme_group)
        output_file = f'{sanatized_theme_name.group(1)}.csv'
    else:
        output_file = f'{theme}.csv'

    #update the ranking number in the new tables
    theme_group['RANK'] = None
    theme_group['RANK'] = range(1, len(theme_group) + 1)



    #if subtheme = ultimate collector series
        #add to ucs table
    #elif subtheme = helmet collection
        #add to helmet table
    #elif subtheme = diorama collection
        #add to diorama collection
    #elif subtheme =

    theme_group.to_csv(output_file, index=False)


    #print(theme_group['PIECES'])
    #print(theme_group)
    #filter and assign values of rows based on the 'Theme' value into seperate dataframes or something

    #break into UCS and Star Wars tables based on Theme

    #generate new subtables based on these rows

    #save excel files seperately

