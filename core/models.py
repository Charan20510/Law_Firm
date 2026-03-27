from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError("The Email field must be set")
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)

		if extra_fields.get("is_staff") is not True:
			raise ValueError("Superuser must have is_staff=True.")
		if extra_fields.get("is_superuser") is not True:
			raise ValueError("Superuser must have is_superuser=True.")

		return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
	ROLE_CLIENT = "client"
	ROLE_ADVOCATE = "advocate"
	ROLE_CHOICES = [
		(ROLE_CLIENT, "Client"),
		(ROLE_ADVOCATE, "Advocate"),
	]

	username = None
	email = models.EmailField(unique=True)
	role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
	phone = models.CharField(max_length=20, blank=True)

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = []
	objects = UserManager()

	def __str__(self):
		return self.email


class ClientProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	father_name = models.CharField(max_length=255)
	dob = models.DateField()
	gender = models.CharField(max_length=20)
	address = models.TextField()
	aadhaar = models.CharField(max_length=20)
	pan = models.CharField(max_length=20)
	photo = models.ImageField(upload_to="client_photos/")
	id_proof = models.FileField(upload_to="client_id_proofs/")
	signature = models.ImageField(upload_to="client_signatures/")

	class Meta:
		verbose_name = "Client Profile"
		verbose_name_plural = "Client Profiles"

	def __str__(self):
		full_name = self.user.get_full_name().strip()
		display_name = full_name or self.user.email
		return f"ClientProfile: {display_name}"


class AdvocateProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	enrollment_number = models.CharField(max_length=100)
	bar_council = models.CharField(max_length=255)
	specialization = models.CharField(max_length=255)
	experience_years = models.PositiveIntegerField()
	office_address = models.TextField()
	photo = models.ImageField(upload_to="advocate_photos/")
	signature = models.ImageField(upload_to="advocate_signatures/")

	class Meta:
		verbose_name = "Advocate Profile"
		verbose_name_plural = "Advocate Profiles"

	def __str__(self):
		full_name = self.user.get_full_name().strip()
		display_name = full_name or self.user.email
		return f"AdvocateProfile: {display_name}"


class Case(models.Model):
	CASE_TYPE_CIVIL = "civil"
	CASE_TYPE_CRIMINAL = "criminal"
	CASE_TYPE_ARBITRATION = "arbitration"
	CASE_TYPE_CHOICES = [
		(CASE_TYPE_CIVIL, "Civil"),
		(CASE_TYPE_CRIMINAL, "Criminal"),
		(CASE_TYPE_ARBITRATION, "Arbitration"),
	]

	STATUS_PENDING = "pending"
	STATUS_CLOSED = "closed"
	STATUS_CHOICES = [
		(STATUS_PENDING, "Pending"),
		(STATUS_CLOSED, "Closed"),
	]

	STAGE_FILING = "filing"
	STAGE_EVIDENCE = "evidence"
	STAGE_ARGUMENT = "argument"
	STAGE_JUDGMENT = "judgment"
	STAGE_CHOICES = [
		(STAGE_FILING, "Filing"),
		(STAGE_EVIDENCE, "Evidence"),
		(STAGE_ARGUMENT, "Argument"),
		(STAGE_JUDGMENT, "Judgment"),
	]

	title = models.CharField(max_length=255)
	case_number = models.CharField(max_length=100)
	case_type = models.CharField(max_length=20, choices=CASE_TYPE_CHOICES)
	court_name = models.CharField(max_length=255)
	client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
	advocate = models.ForeignKey(AdvocateProfile, on_delete=models.CASCADE)
	opponent_details = models.TextField()
	filing_date = models.DateField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)
	stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
	description = models.TextField()

	def __str__(self):
		return f"{self.case_number} - {self.title}"


class Hearing(models.Model):
	STATUS_SCHEDULED = "scheduled"
	STATUS_COMPLETED = "completed"
	STATUS_ADJOURNED = "adjourned"
	STATUS_CHOICES = [
		(STATUS_SCHEDULED, "Scheduled"),
		(STATUS_COMPLETED, "Completed"),
		(STATUS_ADJOURNED, "Adjourned"),
	]

	case = models.ForeignKey(Case, on_delete=models.CASCADE)
	hearing_date = models.DateField()
	next_hearing_date = models.DateField(null=True, blank=True)
	notes = models.TextField()
	judge_remarks = models.TextField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)

	def __str__(self):
		return f"Hearing for {self.case.case_number} on {self.hearing_date}"


class Document(models.Model):
	DOCUMENT_TYPE_EVIDENCE = "evidence"
	DOCUMENT_TYPE_ID = "id"
	DOCUMENT_TYPE_OTHER = "other"
	DOCUMENT_TYPE_CHOICES = [
		(DOCUMENT_TYPE_EVIDENCE, "Evidence"),
		(DOCUMENT_TYPE_ID, "ID"),
		(DOCUMENT_TYPE_OTHER, "Other"),
	]

	case = models.ForeignKey(Case, on_delete=models.CASCADE)
	file = models.FileField(upload_to="case_documents/")
	document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
	notes = models.TextField()
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Document for {self.case.case_number}"


class Task(models.Model):
	STATUS_PENDING = "pending"
	STATUS_DONE = "done"
	STATUS_CHOICES = [
		(STATUS_PENDING, "Pending"),
		(STATUS_DONE, "Done"),
	]

	title = models.CharField(max_length=255)
	case = models.ForeignKey(Case, on_delete=models.CASCADE)
	due_date = models.DateField()
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)

	def __str__(self):
		return self.title
