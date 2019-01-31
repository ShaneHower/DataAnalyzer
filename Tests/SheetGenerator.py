import random
import pandas as pd
from DateGenerator import DateGenerator


class SheetGenerator:
    def __init__(self):
        pass

    def random_selector(self, iter_num, pick_from=None):
        final_list = []
        if pick_from is None:
            for i in range(iter_num):
                pick_from = DateGenerator().generate()
                final_list.append(pick_from)

        for i in range(iter_num):
            if type(pick_from) == int:
                final_list.append(pick_from)
            elif type(pick_from) == list:
                final_list.append(random.choice(pick_from))
        return final_list

    def generate(self, sheets=None):
        if sheets is None:
            sheets = 1

        # acct numbers
        num = random.choice(range(10, 65))
        acct_opt = [11000, 26553, 11885]
        acct_nums = self.random_selector(num, acct_opt)

        # mfg number
        mfg_nums = self.random_selector(num, 9562)

        # dates
        date = self.random_selector(num)

        # unit price
        up_opt = [10, 8]
        unit_prices = self.random_selector(num, up_opt)

        data = {"acct num": acct_nums, "MFG num": mfg_nums, "Date": date, "Unit Price": unit_prices}
        writer = pd.ExcelWriter(r"C:\Users\Shane_Programming\Desktop\AutomatedTests\SheetGenerator\Sheet{0}.xlsx".format(sheets))
        df = pd.DataFrame(data=data)
        df.to_excel(writer)
        writer.save()