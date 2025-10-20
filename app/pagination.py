from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    page_size = 10
    max_page_size = 10000
    page_size_query_param = "count"

    def get_paginated_response(self, context):
        return Response(
            {
                "page": self.page.number,
                "count": self.page.paginator.per_page,
                "total_count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": context,
            }
        )

    def get_paginated_response_schema(self, schema):
        original_schema = super(BasePagination, self).get_paginated_response_schema(
            schema
        )
        response_schema = {
            "type": original_schema["type"],
            "properties": {
                "page": {
                    "type": "integer",
                    "example": 123,
                },
                "total_count": {
                    "type": "integer",
                    "example": 123,
                },
                **original_schema["properties"],
            },
        }
        return response_schema
