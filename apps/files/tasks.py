from django.utils import timezone

from celery import shared_task
from pathlib import Path
from apps.files.models import File
from .services.repair import (
    repair_all_chunks,
)

from .services.node_monitor import (
    check_nodes,
)
from .services.rebalancer import (
    rebalance_cluster,
)




@shared_task
def cleanup_expired_guest_files():

    print("RUNNING CLEANUP TASK")

    files = File.objects.filter(
        is_temporary=True,
        delete_after__lt=timezone.now()
    )

    print(f"FOUND {files.count()} EXPIRED FILES")

    for file_obj in files:

        print(f"DELETING {file_obj.id}")

        if file_obj.file:
            file_obj.file.delete(save=False)

        file_obj.delete()


@shared_task
def test_task():
    print("CELERY IS WORKING!")
    return "success"



@shared_task
def repair_missing_replicas():
    repair_all_chunks()



@shared_task
def monitor_storage_nodes():
    check_nodes()


@shared_task
def rebalance_storage():
    rebalance_cluster()


@shared_task
def remove_original_file(
    file_id
):

    try:

        file_obj = File.objects.get(
            id=file_id
        )

    except File.DoesNotExist:
        return

    if not file_obj.is_distributed:
        return

    if file_obj.file:

        path = Path(
            file_obj.file.path
        )

        if path.exists():

            path.unlink()

        file_obj.file = ""

        file_obj.save(
            update_fields=["file"]
        )