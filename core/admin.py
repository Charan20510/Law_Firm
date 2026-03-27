from django.contrib import admin

from .models import (
	AdvocateProfile,
	Case,
	ClientProfile,
	Document,
	Hearing,
	Task,
	User,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ("email", "role", "phone", "is_staff", "is_active")


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "father_name", "dob", "gender", "aadhaar", "pan")


@admin.register(AdvocateProfile)
class AdvocateProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "enrollment_number", "bar_council", "specialization")


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
	list_display = ("title", "case_number", "case_type", "court_name", "status", "stage")


@admin.register(Hearing)
class HearingAdmin(admin.ModelAdmin):
	list_display = ("case", "hearing_date", "next_hearing_date", "status")


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ("case", "document_type", "uploaded_at")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	list_display = ("title", "case", "due_date", "status")
