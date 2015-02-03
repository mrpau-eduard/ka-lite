from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class TopicNode(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    sort_order = models.FloatField(max_length=50, unique=True, default=0)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['sort_order']