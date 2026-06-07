from django.utils import timezone

from apps.files.models import (
    StorageNode,
)


def send_heartbeat(
    node_name
):

    node = (
        StorageNode.objects
        .get(name=node_name)
    )

    node.last_heartbeat = (
        timezone.now()
    )

    node.save()

    return node