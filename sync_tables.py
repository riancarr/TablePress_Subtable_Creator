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
    #read and format main/initial table
    all_themes_df = pd.read_csv(os.path.join(folder_path, main_table[0]))
    all_themes_df['RANK'] = None  # clear the incorrect rank numbers
    all_themes_df['RANK'] = range(1, len(all_themes_df) + 1)  # fill rank column with incrementing number
    #TODO: check if set number already ends in -1 (currently doesnt so i commented out the next line)
    #all_themes_df['SET NUMBER'] = all_themes_df['SET NUMBER'].astype(str) + '-1' # adds a '-1' to the set number to match the formatting of the brickset csv
    all_themes_df.to_csv(os.path.join(folder_path, main_table[0]), index=False)
elif len(main_table) < 1:
    print('ERROR: No files matching main_table_title. Make sure you have the main table csv in the working directory.')
    quit()
else:
    print('ERROR: Multiple files found matching main_table_title. Make sure you have exactly one main table csv in your working directory.')
    quit()

#TODO parse my brickset page to automatically retrieve the brickset csv
brickset_sets_df = pd.read_csv('Brickset-Sets.csv')
#parse the brickset csv and change the subthemes based on set number
# hardcoded values for modular compatible buildings because they should be considered part of the collection
# change theme for these into creator expert?
# do all this AFTER the creator expert filtering?
unofficial_modular_buildings = ['71799-1', '76269-1', '910023-1', '76218-1', '910013-1', '910009-1', '76178-1']
for index, value in brickset_sets_df['Number'].items():
    brickset_sets_df.loc[brickset_sets_df['Number'].isin(unofficial_modular_buildings), 'Subtheme'] = 'Modular Buildings Collection'
brickset_sets_df.to_csv('Brickset-Sets.csv', index=False)
all_themes_df['Original_Theme'] = all_themes_df['THEME']
all_themes_df.loc[all_themes_df['SET NUMBER'].isin(unofficial_modular_buildings), 'THEME'] = '<a href="https://thebrickboyo.com/set-rankings/creator-expert/" rel="noopener" target="_blank">LEGO Creator Expert</a>'

all_themes_df.to_csv('Test all.csv', index=False)


#format the subtables as needed
#names csv depending on the subtheme name automatically
def format_subtables(subtheme_dataframe, subtheme_name, default_name):
    subtheme_group = subtheme_dataframe.iloc[:, :9]  # removes the merged dataframe parts
    if subtheme_name == 'Helmet Collection' or subtheme_name == 'Starship Collection':
        del subtheme_group['MINIFIGS'] # not needed for these subthemes
    del subtheme_group['THEME']  # remove theme column cus its redundant
    subtheme_group['RANK'] = None  # clear the incorrect rank numbers
    subtheme_group['RANK'] = range(1, len(subtheme_group) + 1)  # fill rank column with incrementing number

    #by process of filtering the other subthemes, the remaining take the value of the theme-specific 'default' name (determined before being passed to here)
    #necessary to do because playsets official subthemes stretch across LOADS of values
    if subtheme_name == 'Other':
        subtheme_group.to_csv(f'{default_name}.csv', index=False)
    else:
        subtheme_group.to_csv(f'{subtheme_name}.csv', index=False)

#further divide themes into subtables
def divide_into_subtables(theme, theme_group):
    #merges the brickset collection csv with the tablepress table to retrieve the subtheme
    #this subtheme will be used to split the table into more subtables (ie more csv files)
    merged_df = pd.merge(theme_group, brickset_sets_df, left_on='SET NUMBER', right_on='Number', how='inner')


    #hardcoded values for brick built characters (move later for easier modification)
    #these need to be hardcoded cus its an arbitrary subtheme i made up
    brick_built_characters = ['75308-1', '75306-1', '75335-1', '75318-1', '75230-1', '75255-1', '75187-1']
    merged_df.loc[merged_df['Number'].isin(brick_built_characters), 'Subtheme'] = 'Brick-Built Character'


    # changed all non-relevant subtheme values for the sake of unity
    # this was needed because otherwise all 'playsets' would be split across multiple subthemes like 'Episode 4'/'Clone Wars' etc
    subthemes_to_keep = ['Ultimate Collector Series', 'Helmet Collection', 'Diorama Collection', 'Modular Buildings Collection', 'Vehicles', 'Brick-Built Character', 'Starship Collection']
    merged_df.loc[~merged_df['Subtheme'].isin(subthemes_to_keep), 'Subtheme'] = 'Other'  # the tilda thing is a NOT operation so it reverses the outcome of this kinda

    if theme == 'LEGO Star Wars':
    #divide into helmets, dioramas, ucs and playsets
        subtheme_default_name = 'Star Wars Playsets'  # the name given to the 'Other' subthemes once the main ones have been filtered

    elif theme == 'LEGO Creator Expert':  #PROBLEM: the modular buildings across different themes dont combine into one for the modular buildings output
    #divide into modular buildings and vehicles
        subtheme_default_name = 'Remaining Icons'  # the name given to the 'Other' subthemes once the main ones have been filtered

    #format the subtables created from the subthemes
    merged_df_groups = merged_df.groupby('Subtheme')
    for subtheme, subtheme_group in merged_df_groups:
        format_subtables(subtheme_group, subtheme, subtheme_default_name)


#group by theme
theme_groups = all_themes_df.groupby('THEME')

for theme, theme_group in theme_groups:
    if '<a href' in theme:
        sanatized_theme_name = re.search(r'>([^<]+)</a>', theme)
        if sanatized_theme_name.group(1) == 'LEGO Star Wars' or sanatized_theme_name.group(1) == 'LEGO Creator Expert':
            divide_into_subtables(sanatized_theme_name.group(1), theme_group)
        output_file = f'{sanatized_theme_name.group(1)}.csv'
    else:
        output_file = f'{theme}.csv'

    #update the ranking number in the new tables
    theme_group['RANK'] = None
    theme_group['RANK'] = range(1, len(theme_group) + 1)

    #restore theme values to their originals (needed to remove modular compatible sets from other themes)
    theme_group['THEME'] = None  #clear the 'THEME' column
    theme_group['THEME'] = all_themes_df['Original_Theme']  #restore the original 'Theme' values
    #maybe loop through theme group and remove anything with a mismatched theme?
    theme_group = theme_group.iloc[:, :9] #remove the Original Theme column from output

    theme_group.to_csv(output_file, index=False)





