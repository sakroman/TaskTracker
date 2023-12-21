from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = ['user', 'id', 'title', 'description', 'due_date']
