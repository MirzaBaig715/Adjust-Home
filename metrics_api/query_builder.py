from metrics_api.utils.constants import common as Constant
from metrics_api.models import Metric
from django.db import models as aggregator
from collections import ChainMap


class QueryBuilder:
    """
    Class to build dynamic query with the given attributes
    """

    def __init__(self, **kwargs):
        """
        Initialize class attributes
        """
        self.selectors = kwargs.get("selectors", [])
        self.filters = kwargs.get("filters", {})
        self.aggregated_fields_list = []
        self.selected_fields_list = []
        self.sort_by = kwargs.get("sort_by", [])
        self.sort_order = kwargs.get("sort_order", "asc").lower()
        self.group_by = kwargs.get("group_by")
        self.metric = Metric.objects.filter(**self.filters)

    def process_and_set_annotations(self):
        """
        process aggregation and selection fields in selectors

        1. Handle special fields like cpi and in order for other non model fields we can add in special_field_dict
           and specify correct formula which can be in (sum. count, average)

        2. Handle fields with no operation value and also not in group_by mentioned (sql query is not valid in this case).
              - we add SUM operation if field has no operation value and also not present in group_by (if group_by specified)

        (sql error) ==>  SELECT spend  FROM metric WHERE country = 'CA' GROUP BY channel;

        (correct) ==> SELECT SUM(spend)  FROM metric WHERE country = 'CA' GROUP BY channel;

        NOTE: please add operation in selectors if you are using group by and Model field is not present in group by (except ).
        """
        reducer_list = []
        for item in self.selectors:
            _field = item.get("field")
            operation = item.get("operation", "").lower()
            # fields to return in response
            self.selected_fields_list.append(_field)

            if _field in Constant.non_operational_fields:
                # fields that cannot be process with aggregations
                operation = Constant.F

            if _field and _field in Constant.non_models_fields:
                # handle special fields like cpi
                operation = Constant.SUM if self.group_by else Constant.F
                reducer = getattr(aggregator, Constant.AGGREGATOR_DICT[operation])
                special_field_dict = {'cpi': [{Constant.model_fields_dict[_field]: reducer('spend') / reducer('installs')}]}
                reducer_list.extend(special_field_dict[_field])
                self.aggregated_fields_list.append(_field)
            elif _field:
                if not operation:
                    operation = Constant.SUM if self.group_by else Constant.F
                reducer = getattr(aggregator, Constant.AGGREGATOR_DICT[operation])
                reducer_list.append({Constant.model_fields_dict[_field]: reducer(_field)})
                self.aggregated_fields_list.append(_field)
        if reducer_list:
            self.metric = self.metric.annotate(**ChainMap(*reducer_list[::-1]))

    def set_group_by(self):
        """
        Set the group_by
        """
        self.metric = self.metric.values(*self.group_by)

    def set_order_by(self):
        """
        Set the order by of model/non-model fields
        """
        if self.sort_by in self.aggregated_fields_list:
            self.sort_by = Constant.model_fields_dict[self.sort_by]
        self.metric = self.metric.order_by(Constant.SORTING[self.sort_order].format(sort_order=self.sort_by))

    def process_and_get_metrics(self):
        """
        process and evaluate the metric objects in list
        :return: list of objects, selected fields
        """
        self.set_group_by()
        if self.selectors:
            self.process_and_set_annotations()
        if self.sort_by:
            self.set_order_by()

        print(self.metric.query)
        return self.metric, self.selected_fields_list