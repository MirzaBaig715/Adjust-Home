from rest_framework import serializers, status
from metrics_api.models import Metric
from metrics_api.utils.constants.response import ResponseMessages
from metrics_api.utils.constants import common as Constant
from metrics_api.utils.response import CustomResponse


class SelectorSerializer(serializers.Serializer):
    """
    Validate selectors in a query
    """
    field = serializers.CharField(required=False, allow_blank=True)
    operation = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        fields = ['field', 'operation']

    def validate_field(self, attr):
            if not hasattr(Metric, attr) and attr not in Constant.non_models_fields:
                raise CustomResponse(
                    message=ResponseMessages.INVALID_DATA.format(object=attr),
                    code=status.HTTP_400_BAD_REQUEST
                ).error()
            return attr

    def validate_operation(self, attr):
        attr = str(attr)
        if attr and attr.lower() not in Constant.AGGREGATOR_DICT.keys():
            raise CustomResponse(
                message=ResponseMessages.INVALID_DATA.format(object=attr),
                code=status.HTTP_400_BAD_REQUEST
            ).error()
        return attr
    def validate(self, attrs):
        _field = str(attrs.get('field'))
        _operation = str(attrs.get('operation'))

        if not hasattr(Metric, _field) and _field not in Constant.non_models_fields:
            raise CustomResponse(
                message=ResponseMessages.INVALID_DATA.format(object=_field),
                code=status.HTTP_400_BAD_REQUEST
            ).error()

        if _operation and _operation.lower() not in Constant.AGGREGATOR_DICT.keys():
            raise CustomResponse(
                message=ResponseMessages.INVALID_DATA.format(object=_operation),
                code=status.HTTP_400_BAD_REQUEST
            ).error()

        if _operation and _field in Constant.non_models_fields:
            if not Constant.AGGREGATOR_DICT.get(_operation):
                raise CustomResponse(
                    message=ResponseMessages.OPERATION_NOT_ALLOWED.format(object=_field),
                    code=status.HTTP_400_BAD_REQUEST
                ).error()

        return attrs


class ValidateRequestSerializer(serializers.Serializer):
    """
    Validate incoming data from request and show errors if data is not correct
    """
    selectors = SelectorSerializer(many=True, required=False)
    filters = serializers.DictField(required=False)
    sort_by = serializers.CharField(required=False, allow_blank=True)
    sort_order = serializers.CharField(required=False, allow_blank=True)
    group_by = serializers.ListField(required=False)

    class Meta:
        fields = ['selectors', 'filters', 'sort_by', 'sort_order', 'group_by']

    def validate(self, attrs):
        _filters = attrs.get('filters', {})
        _sorting = attrs.get('sort_order')
        _group_by = attrs.get('group_by', [])
        is_error = False
        error_field = ''
        for _field in _filters:
            if not (hasattr(Metric, _field) or _field in Constant.ALLOW_DATE_FORMATS):
                is_error = True
                error_field = _field
                break

        if _sorting and _sorting.lower() not in Constant.SORTING.keys():
            is_error = True
            error_field = _sorting

        for _field in _group_by:
            if not (_field in Constant.model_fields_dict.keys() or _field in Constant.non_models_fields):
                is_error = True
                error_field = _field

        if is_error:
            raise CustomResponse(
                message=ResponseMessages.INVALID_DATA.format(object=error_field),
                code=status.HTTP_400_BAD_REQUEST
            ).error()
        return attrs


class MetricSerializer(serializers.ModelSerializer):
    """
    Metric Serializer to perform object related actions
    """
    cpi = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Metric
        fields = ['id', 'spend', 'cpi', 'channel', 'installs', 'country', 'impressions', 'clicks', 'revenue']

    def to_representation(self, instance):
        _fields = self.context.get('_fields')
        data = {}
        for item, value in instance.items():
            if Constant.model_fields_dict[item] in _fields:
                data.update({Constant.model_fields_dict[item]: value})
        return data