# -*- coding: utf-8 -*-
import pandas as pd
from brightway2 import get_activity

from .dataframe_table import ABDataFrameTable


class LCAResultsTable(ABDataFrameTable):
    @ABDataFrameTable.decorated_sync
    def sync(self, lca):
        col_labels = [" | ".join(x) for x in lca.methods]
        row_labels = [str(get_activity(list(func_unit.keys())[0])) for func_unit in lca.func_units]
        self.dataframe = pd.DataFrame(lca.results, index=row_labels, columns=col_labels)


class ProcessContributionsTable(ABDataFrameTable):
    def __init__(self, parent):
        super(ProcessContributionsTable, self).__init__(parent)
        self.parent = parent

    @ABDataFrameTable.decorated_sync
    def sync(self, dummy):
        self.dataframe = self.parent.plot.df_tc

class InventoryCharacterisationTable(ABDataFrameTable):
    def __init__(self, parent):
        super(InventoryCharacterisationTable, self).__init__(parent)
        self.parent = parent

    @ABDataFrameTable.decorated_sync
    def sync(self, dummy):
        self.dataframe = self.parent.plot.df_tc


class InventoryTable(ABDataFrameTable):
    @ABDataFrameTable.decorated_sync
    def sync(self, mlca, method=None, limit=18):
        key = method
        array = mlca.technosphere_flows[key]
        max_length = limit
        length = min(max_length, len(array))
        labels = [get_activity(mlca.rev_activity_dict[i]) for i in range(length)]
        col_labels = ['Amount']
        row_labels = [str(i) for i in labels[:length]]
        self.dataframe = pd.DataFrame(array[:length], index=row_labels, columns=col_labels)

        self.setVerticalScrollMode(1)
        self.setHorizontalScrollMode(1)