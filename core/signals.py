from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import AdvocateProfile, Case, ClientProfile, Document, Hearing, Task
from .utils.email_notifications import send_model_change_email


TRACKED_MODELS = (ClientProfile, AdvocateProfile, Case, Hearing, Document, Task)
_OLD_STATE = {}


def _serialize_instance(instance):
    data = {}
    for field in instance._meta.fields:
        data[field.name] = field.value_from_object(instance)
    return data


def _format_value(value):
    if value is None:
        return ""
    return str(value)


def _get_changed_fields(instance, old_data, new_data):
    changed = []
    for field in instance._meta.fields:
        if field.name == "id":
            continue
        field_name = field.verbose_name.title()
        old_value = old_data.get(field.name)
        new_value = new_data.get(field.name)
        if old_value != new_value:
            changed.append((field_name, _format_value(old_value), _format_value(new_value)))
    return changed


@receiver(pre_save, sender=ClientProfile)
@receiver(pre_save, sender=AdvocateProfile)
@receiver(pre_save, sender=Case)
@receiver(pre_save, sender=Hearing)
@receiver(pre_save, sender=Document)
@receiver(pre_save, sender=Task)
def capture_old_state(sender, instance, **kwargs):
    if not instance.pk:
        return
    previous = sender.objects.filter(pk=instance.pk).first()
    if previous is None:
        return
    _OLD_STATE[(sender.__name__, instance.pk)] = _serialize_instance(previous)


@receiver(post_save, sender=ClientProfile)
@receiver(post_save, sender=AdvocateProfile)
@receiver(post_save, sender=Case)
@receiver(post_save, sender=Hearing)
@receiver(post_save, sender=Document)
@receiver(post_save, sender=Task)
def handle_save(sender, instance, created, **kwargs):
    if created:
        return

    model_name = sender.__name__
    old_data = _OLD_STATE.pop((model_name, instance.pk), {})
    new_data = _serialize_instance(instance)
    changed_fields = _get_changed_fields(instance, old_data, new_data)
    if not changed_fields:
        return

    send_model_change_email(
        model_name=model_name,
        action="Updated",
        record_id=instance.pk,
        changed_fields=changed_fields,
    )
