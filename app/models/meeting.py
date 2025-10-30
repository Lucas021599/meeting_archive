from django.db import models


class Meeting(models.Model):
    category = models.CharField(max_length=50, help_text="회의 대주제")
    title = models.CharField(max_length=255, help_text="회의명")
    summary = models.TextField(help_text="회의 요약")
    meeting_date = models.DateField(help_text="회의 날짜")

    class Meta:
        managed = True
        db_table = "meeting"
