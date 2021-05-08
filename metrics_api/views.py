from rest_framework import generics, status

from metrics_api.query_builder import QueryBuilder
from metrics_api.serializers import MetricSerializer, ValidateRequestSerializer
from .utils.response import CustomResponse


class MetricsAPIView(generics.GenericAPIView):
    """
    Metric Api view to get the metrics according to the given data
    """
    serializer_class = ValidateRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serialized_data = serializer.data
            try:
                import json
                metrics, _fields = QueryBuilder(**serialized_data).process_and_get_metrics()
            except Exception as exception:
                return CustomResponse(
                    message=str(exception),
                    code=status.HTTP_400_BAD_REQUEST
                ).response()

            data = MetricSerializer(metrics, many=True, context={'_fields': _fields}).data
            return CustomResponse(data=data).response()
        return CustomResponse(code=status.HTTP_400_BAD_REQUEST).response()
