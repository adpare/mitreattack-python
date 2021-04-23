try:
    from ..core.exceptions import typeChecker, categoryChecker, UNSETVALUE
except ImportError:
    from core.exceptions import typeChecker, categoryChecker, UNSETVALUE

from enum import Enum


class Aggregates(Enum):
    average = 1
    min = 2
    max = 3
    sum = 4


class Layout:
    def __init__(self):
        """
            Initialization - Creates a layout object
        """
        self.__layout = UNSETVALUE
        self.__showID = UNSETVALUE
        self.__showName = UNSETVALUE
        self.__showAggregateScores = UNSETVALUE
        self.__countUnscored = UNSETVALUE
        self.__aggregateFunction = Aggregates.average

    def compute_aggregate(self, technique, subtechniques):
        """
            Compute the aggregate score for a technique and any subtechniques
            :param technique: The chosen technique object
            :param subtechniques: Any relevant subtechnique objects
            :return: Integer representing aggregate score (or None if not computable)
        """
        scores = []
        if self.showAggregateScores:
            if technique.score is not None:
                scores = [technique.score]
            for x in subtechniques:
                if x.score is not None:
                    scores.append(x.score)
                elif self.countUnscored:
                    scores.append(0)
            if all(x == 0 for x in scores):
                return None
            modified = self.aggFunction(scores)
            return modified
        else:
            return None

    def aggFunction(self, data_block):
        """
            Apply the selected aggregate function to a data_block
            :param data_block: List containing scores to compute over (generated by compute_aggregate)
            :return: Calculated score
        """
        if self.showAggregateScores:
            data = data_block

            if self.__aggregateFunction == Aggregates.average:
                return sum(data)/len(data)
            elif self.__aggregateFunction == Aggregates.min:
                return min(data)
            elif self.__aggregateFunction == Aggregates.max:
                return max(data)
            elif self.__aggregateFunction == Aggregates.sum:
                return sum(data)

    @property
    def layout(self):
        if self.__layout != UNSETVALUE:
            return self.__layout

    @layout.setter
    def layout(self, layout):
        typeChecker(type(self).__name__, layout, str, "layout")
        categoryChecker(type(self).__name__, layout, ["side", "flat", "mini"],
                        "layout")
        self.__layout = layout

    @property
    def showID(self):
        if self.__showID != UNSETVALUE:
            return self.__showID

    @showID.setter
    def showID(self, showID):
        typeChecker(type(self).__name__, showID, bool, "showID")
        self.__showID = showID

    @property
    def showName(self):
        if self.__showName != UNSETVALUE:
            return self.__showName

    @showName.setter
    def showName(self, showName):
        typeChecker(type(self).__name__, showName, bool, "showName")
        self.__showName = showName

    @property
    def showAggregateScores(self):
        if self.__showAggregateScores != UNSETVALUE:
            return self.__showAggregateScores

    @showAggregateScores.setter
    def showAggregateScores(self, showAggregateScores):
        typeChecker(type(self).__name__, showAggregateScores, bool,
                    "showAggregateScores")
        self.__showAggregateScores = showAggregateScores

    @property
    def countUnscored(self):
        if self.__countUnscored != UNSETVALUE:
            return self.__countUnscored

    @countUnscored.setter
    def countUnscored(self, countUnscored):
        typeChecker(type(self).__name__, countUnscored, bool, "countUnscored")
        self.__countUnscored = countUnscored

    @property
    def aggregateFunction(self):
        if self.__aggregateFunction == Aggregates.average:
            return "average"
        elif self.__aggregateFunction == Aggregates.min:
            return "min"
        elif self.__aggregateFunction == Aggregates.max:
            return "max"
        elif self.__aggregateFunction == Aggregates.sum:
            return "sum"

    @aggregateFunction.setter
    def aggregateFunction(self, aggregateFunction):
        categoryChecker(type(self).__name__, aggregateFunction.lower(),
                        ["average", "min", "max", "sum"], "aggregateFunction")
        self.__aggregateFunction = Aggregates[aggregateFunction.lower()]

    def get_dict(self):
        """
            Converts the currently loaded data into a dict
            :returns: A dict representation of the local layout object
        """
        listing = vars(self)
        temp = dict()
        for entry in listing:
            if listing[entry] != UNSETVALUE:
                temp[entry.split(type(self).__name__ + '__')[-1]]\
                    = listing[entry]
        if len(temp) > 0:
            return temp