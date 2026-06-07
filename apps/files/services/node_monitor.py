from datetime import timedelta

from django.utils import timezone

from apps.files.models import (
    StorageNode,
)


HEARTBEAT_TIMEOUT = (
    timedelta(minutes=2)
)


def check_nodes():

    now = timezone.now()

    nodes = (
        StorageNode.objects.all()
    )

    for node in nodes:

        if (
            node.last_heartbeat
            and now
            - node.last_heartbeat
            > HEARTBEAT_TIMEOUT
        ):

            node.is_active = False

            node.save(
                update_fields=[
                    "is_active"
                ]
            )