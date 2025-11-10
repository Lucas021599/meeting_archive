from qdrant_client.models import FieldCondition, Filter, MatchValue

from meeting_archive.qdrant import get_qdrant_client
from meeting_archive.settings import COLLECTION_NAME, SENTENCE_MODEL


def embed_text(text):
    return SENTENCE_MODEL.encode(text).tolist()


# category 및 query 기준으로 검색 결과 반환
def query_points(category, query):
    client = get_qdrant_client()
    result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embed_text(query),
        limit=30,
        query_filter=(
            Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category),
                    ),
                ],
            )
            if category
            else None
        ),
    )
    return result


# meeting_id 기준으로 합산 점수 계산, meeting_id 리스트 반환
def calculate_points_score(points):
    point_scores = {}
    for point in points:
        meeting_id = point.payload.get("meeting_id")
        point_scores[meeting_id] = point_scores.get(meeting_id, 0) + point.score
    point_scores = sorted(
        point_scores.items(), key=lambda x: (x[1], x[0]), reverse=True
    )
    return [meeting_id for meeting_id, _ in point_scores]
