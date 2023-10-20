import pandas as pd
import regex as re
import os

#def divide_into_subtables(all_themes, subthemes_list):

#read in main file
all_themes_df = pd.read_csv('45-All-Themes-Set-Ranking-2023-10-02.csv')


#group by theme
theme_groups = all_themes_df.groupby('THEME')

for theme, theme_group in theme_groups:
    if '<a href' in theme:
        sanatized_theme_name = re.search(r'>([^<]+)</a>', theme)
        print(sanatized_theme_name.group(1))
        output_file = f'{sanatized_theme_name.group(1)}.csv'
    else:
        output_file = f'{theme}.csv'

    #update the ranking number in the new tables
    theme_group['RANK'] = None
    theme_group['RANK'] = range(1, len(theme_group) + 1)

    theme_group.to_csv(output_file, index=False)


    #print(theme_group['PIECES'])
    #print(theme_group)
    #filter and assign values of rows based on the 'Theme' value into seperate dataframes or something

    #break into UCS and Star Wars tables based on Theme

    #generate new subtables based on these rows

    #save excel files seperately