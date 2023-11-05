import pandas as pd
import regex as re
import os


#read in main file by removing the timestamp appendage
folder_path = os.getcwd()
files = os.listdir(folder_path)

#find main table in directory
main_table_title = '45-All-Themes-Set-Ranking'
main_table = [file_name for file_name in files if main_table_title in file_name]

#make sure theres only one main table
#TODO automatically pick newest date/largest file in the case of multiple main files
if len(main_table) == 1:
    all_themes_df = pd.read_csv(os.path.join(folder_path, main_table[0]))
elif len(main_table) < 1:
    print('ERROR: No files matching main_table_title. Make sure you have the main table csv in the working directory.')
    quit()
else:
    print('ERROR: Multiple files found matching main_table_title. Make sure you have exactly one main table csv in your working directory.')
    quit()
brickset_sets_df = pd.read_csv('Brickset-Sets.csv')

#adds a '-1' to the set number to match the formatting of the brickset csv
all_themes_df['SET NUMBER'] = all_themes_df['SET NUMBER'].astype(str) + '-1'
all_themes_df.to_csv('Test all.csv', index=False)


#format the subtables as needed
#names csv depending on the subtheme name automatically
def format_subtables(subtheme_dataframe, subtheme_name):
    subtheme_group = subtheme_dataframe.iloc[:, :9]  # removes the merged dataframe parts
    if subtheme_name == 'Helmet Collection' or subtheme_name == 'Midi-Scale Collection':
        del subtheme_group['MINIFIGS'] # not needed for these subthemes
    del subtheme_group['THEME']  # remove theme column cus its redundant
    subtheme_group['RANK'] = None  # clear the incorrect rank numbers
    subtheme_group['RANK'] = range(1, len(subtheme_group) + 1)  # fill rank column with incrementing number

    #by process of filtering the other subthemes, the remaining are playsets
    #necessary to do because playsets official subthemes stretch across LOADS of values
    if subtheme_name == 'Other':
        subtheme_group.to_csv('Star Wars Playsets.csv', index=False)
    else:
        subtheme_group.to_csv(f'{subtheme_name}.csv', index=False)

#further divide themes into subtables
def divide_into_subtables(theme, theme_group):
    #merges the brickset collection csv with the tablepress table to retrieve the subtheme
    #this subtheme will be used to split the table into more subtables (ie more csv files)
    merged_df = pd.merge(theme_group, brickset_sets_df, left_on='SET NUMBER', right_on='Number', how='inner')

    #changed all non-relevant subtheme values for the sake of unity
    #this was needed because otherwise all 'playsets' would be split across multiple subthemes like 'Episode 4'/'Clone Wars' etc
    subthemes_to_keep = ['Ultimate Collector Series', 'Helmet Collection', 'Diorama Collection']
    merged_df.loc[~merged_df['Subtheme'].isin(subthemes_to_keep), 'Subtheme'] = 'Other' #the tilda thing is a NOT operation so it reverses the outcome of this kinda

    #hardcoded values for brick built characters (move later for easier modification)
    #these need to be hardcoded cus its an arbitrary subtheme i made up
    brick_built_characters = ['75308-1', '75306-1', '75335-1', '75318-1', '75230-1', '75255-1', '75187-1']
    merged_df.loc[merged_df['Number'].isin(brick_built_characters), 'Subtheme'] = 'Brick-Built Character'

    #hardcoded values for midi scale sets because they ALSO arent official on bricksets csv
    midi_scale_collection = ['75356-1']
    merged_df.loc[merged_df['Number'].isin(midi_scale_collection), 'Subtheme'] = 'Midi-Scale Collection'

    if theme == 'LEGO Star Wars':
    #divide into helmets, dioramas, ucs and playsets
        merged_df_groups = merged_df.groupby('Subtheme')
        for subtheme, subtheme_group in merged_df_groups:
            format_subtables(subtheme_group, subtheme)
    #elif theme == 'LEGO Creator Expert':



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


    theme_group.to_csv(output_file, index=False)





