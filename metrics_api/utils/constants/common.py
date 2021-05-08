non_models_fields = ['cpi']
model_fields_dict = {
    '_spend': 'spend', 'spend': '_spend',
    '_impressions': 'impressions', 'impressions': '_impressions',
    '_clicks': 'clicks', 'clicks': '_clicks',
    '_revenue': 'revenue', 'revenue': '_revenue',
    '_installs': 'installs', 'installs': '_installs',
    '_channel': 'channel', 'channel': '_channel',
    '_country': 'country', 'country': '_country',
    '_os': 'os', 'os': '_os', '_cpi': 'cpi', 'cpi': '_cpi',
    '_date': 'date', 'date': '_date',
    '_id': 'id', 'id': '_id'
}
non_operational_fields = ['channel', 'country', 'os', 'date']
AGGREGATOR_DICT = {'sum': 'Sum', 'average': 'Avg', 'count': 'Count', 'f': 'F'}
SUM = 'sum'
F = 'f'

SORTING = {
    'desc': '-{sort_order}',
    'asc': '{sort_order}'
}
ALLOW_DATE_FORMATS = ['date__lt','date__gt','date__range', 'date__month', 'date__year', 'date__day']