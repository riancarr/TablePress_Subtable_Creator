import pandas as pd
import regex as re
import os


#read in main file
all_themes_df = pd.read_csv('45-All-Themes-Set-Ranking-2023-10-02.csv')
brickset_sets_df = pd.read_csv('Brickset-Sets.csv')

#adds a '-1' to the set number to match the formatting of the brickset csv
all_themes_df['SET NUMBER'] = all_themes_df['SET NUMBER'].astype(str) + '-1'
all_themes_df.to_csv('Test all.csv', index=False)

#further divide themes into subtables
def divide_into_subtables(theme, theme_group):
    #merges the brickset collection csv with the tablepress table to retrieve the subtheme
    #this subtheme will be used to split the table into more subtables (ie more csv files)
    merged_df = pd.merge(theme_group, brickset_sets_df, left_on='SET NUMBER', right_on='Number', how='inner')
    #merged_df.to_csv('TestMerge.csv', index=False)

    if theme == 'LEGO Star Wars':
    #divide into helmets, dioramas, ucs and playsets
        merged_df_groups = merged_df.groupby('Subtheme')
        for subtheme, subtheme_group in merged_df_groups:
            if subtheme == 'Ultimate Collector Series':
                subtheme_group = subtheme_group.iloc[:, :9] #removes the merged dataframe parts
                del subtheme_group['THEME'] #remove theme column cus its redundant
                subtheme_group['RANK'] = None #clear the incorrect rank numbers
                subtheme_group['RANK'] = range(1, len(subtheme_group) + 1) #fill rank column with incrementing number
                subtheme_group.to_csv('Ultimate Collector Series.csv', index=False)

    #elif theme == 'LEGO Creator Expert':


    #elif theme == 'LEGO Star Wars':
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

