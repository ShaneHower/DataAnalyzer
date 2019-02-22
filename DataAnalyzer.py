import pandas as pd
from ListAnalyzer import ListAnalyzer

""" 
    Currently:
    - this program, takes sheet, filters through acct numbers, which filter through part numbers
    - orders by date
    - then finds all variances with minimum charged for each part
    - filters and isolates those indices
    - determines if the max is included (this would suggest that it is a price increase, we don't want these)
    - if max is there, first checks if it has a consecutive sequence before it (it will take out the whole sequence if this is the case
    - it then splits the remainder of the list of indices into groups of consecutive sequences (in order to isolate those rows)
    - it iterates through this new list of lists of indices and grabs the row before the min and after the max to dump 
      into the new excel sheet
    - deletes duplicates based on index 
    
    possible issue (that may not be an issue)
    - if the date of service is exactly the same day for the same account and same part, I don't see this ever occuring 
      but these instances have the potential of getting missed. 
      
    Other Notes:
    Needs to have access to ListAnalyzer to work.
"""


class DataAnalyzer:
    def __init__(self, save_file, path, sheet, col_date, col_acct, col_part, col_price, col_extpr):
        self.col_date = col_date
        self.col_acct = col_acct
        self.col_part = col_part
        self.col_price = col_price
        self.col_extpr = col_extpr

        # set up excel sheet for uploading
        self.writer = pd.ExcelWriter(r"{0}.xlsx".format(save_file))

        # grab data
        self.df = pd.read_excel(r"{0}".format(path), sheet_name=sheet)
        print("file received: {0}".format(path))

    def find_descr(self):
        # needs to happen because the indices must be in order when I filter them later
        df2 = self.df.sort_values(by=[self.col_date], ascending=True)

        # get list of all part numbers and cycle through it
        acct_num = list(self.df[self.col_acct].unique())

        # make an empty DF to keep appending filtered data
        df_to_upload = pd.DataFrame()
        print("entering loop")

        # iterate through acct numbers, for each acct number iterate through the part numbers and filter by that part
        for acct in acct_num:
            df3 = df2[df2[self.col_acct] == acct]
            # grab the list of unique part numbers per acct number to filter through
            part_numbers = list(df3[self.col_part].unique())
            for num in part_numbers:
                print("part number: {0}".format(num))
                df4 = df3[df3[self.col_part] == num]
                df4 = df4[df4[self.col_extpr] > 0]
                df4["Var with Min"] = df4[self.col_price] - df4[self.col_price].min()
                df4["Deviation"] = df4[self.col_price] - df4[self.col_price].mean()
                df4["Z Score"] = df4["Deviation"] / df4[self.col_price].std()

                # need to reset index because this is the way I'm going to grab the range of values I need
                df4 = df4.reset_index()

                # filtering the non zero var so I can pull their indices and dump them in a list
                #  which allows me to pull min and max for iloc filtering
                df_index_finder = df4[df4["Var with Min"] != 0]
                # df_index_finder = df4[df4["Z Score"] > 1]
                indices = df_index_finder.index.values.tolist()
                print("unclean indices: {0}".format(indices))
                # takes out the max if goes over count has to happen here because it may return an empty list
                if (indices != []) and (max(indices) >= len(df4.index) - 1):
                    inst = ListAnalyzer(indices)
                    indices = inst.delete_max()
                print("clean indices: {0}".format(indices))

                # filters out low-high pricing
                if indices != []:
                    # Grouped indices by sequences then iterate through this list to grab the correct rows
                    indices_grouped = ListAnalyzer(indices).find_sequence()

                    for seq_list in indices_grouped:
                        print("seq_list: {0}".format(seq_list))
                        if min(seq_list) != 0:
                            df5 = df4.iloc[min(seq_list) - 1: max(seq_list) + 2]
                            df5.set_value(min(seq_list) - 1, "Var with Min", 0)
                            df5.set_value(max(seq_list) + 1, "Var with Min", 0)
                        else:
                            df5 = df4.iloc[min(seq_list): max(seq_list) + 2]
                            df5.set_value(max(seq_list) + 1, "Var with Min", 0)
                        df5 = df5.drop_duplicates(subset=["index"], keep=False)
                        df_to_upload = df_to_upload.append(df5)

        # sort all of this stuff so user doesn't have to should be done before saving this is redundant
        # df_to_upload = df_to_upload.sort_values(by=[self.col_acct, self.col_part, self.col_date], ascending=True)
        df_to_upload.to_excel(self.writer, "Sheet1")
        self.writer.save()
