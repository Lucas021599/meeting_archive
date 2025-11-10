import uuid

from qdrant_client.models import FieldCondition, Filter, MatchValue, PointStruct

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


# meeting_id 기준으로 point 삭제
def qdrant_delete(meeting_id):
    client = get_qdrant_client()
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="meeting_id",
                    match=MatchValue(value=meeting_id),
                ),
            ],
        ),
    )


# meeting_id 기준으로 payload 업데이트
def qdrant_update_payload(meeting_id, payload):
    client = get_qdrant_client()
    client.set_payload(
        collection_name=COLLECTION_NAME,
        points=Filter(
            must=[
                FieldCondition(
                    key="meeting_id",
                    match=MatchValue(value=meeting_id),
                ),
            ],
        ),
        payload=payload,
    )


# meeting 데이터 삽입
def qdrant_upsert(data):
    """
    Args:
        data (dict): Meeting data to insert in Qdrant.
            - text (str): Meeting summary
            - meeting_id (str): Meeting ID
            - category (str): Meeting category
    """
    embedding = embed_text(data["text"])
    client = get_qdrant_client()
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload=data,
            ),
        ],
    )
