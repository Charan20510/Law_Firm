from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


def send_model_change_email(model_name, action, record_id, changed_fields=None):
    recipients = getattr(settings, "AUTOMATION_NOTIFICATION_EMAILS", [])
    sender = getattr(settings, "DEFAULT_FROM_EMAIL", "") or getattr(settings, "EMAIL_HOST_USER", "")
    if not recipients or not sender:
        return

    timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    subject = f"[Legal Portal] {model_name} {action}"

    body_lines = [
        "Legal Portal Automation Notification",
        "",
        f"Model Name: {model_name}",
        f"Action: {action}",
        f"Record ID: {record_id}",
        f"Timestamp: {timestamp}",
    ]

    if action == "Updated" and changed_fields:
        body_lines.append("")
        body_lines.append("Changed Fields:")
        for field_name, old_value, new_value in changed_fields:
            body_lines.append(f"{field_name}: {old_value} -> {new_value}")

    message = "\n".join(body_lines)
    send_mail(
        subject=subject,
        message=message,
        from_email=sender,
        recipient_list=recipients,
        fail_silently=True,
    )
