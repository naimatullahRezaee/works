from django.db import models
from accounts.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Action(models.Model):
    user = models.ForeignKey(User, related_name="actions", on_delete=models.CASCADE)
    verb = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    target_obj = models.ForeignKey(ContentType, blank=True, null=True, related_name="target_obj", on_delete=models.CASCADE)
    target_id   = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_obj', 'target_id')

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_obj', 'target_id']),
        ]

        ordering = ['-created']


class OpenedAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    open = models.BooleanField(default=False)
    opened_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} watches {self.action.verb}"