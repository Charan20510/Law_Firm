from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from io import BytesIO

from .forms import (
	AdvocateProfileForm,
	CaseForm,
	ClientProfileForm,
	DocumentForm,
	HearingForm,
	LoginForm,
	SignUpForm,
	TaskForm,
)
from .models import AdvocateProfile, Case, ClientProfile, Document, Hearing, Task


def landing(request):
	if request.user.is_authenticated:
		return redirect("dashboard")
	return render(request, "landing.html")


def signup_view(request):
	if request.user.is_authenticated:
		return redirect("dashboard")

	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Signup successful. Please log in.")
			return redirect("login")
	else:
		form = SignUpForm()

	return render(request, "form.html", {"form": form, "title": "Sign Up"})


def login_view(request):
	if request.user.is_authenticated:
		return redirect("dashboard")

	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password"]
			user = authenticate(request, username=email, password=password)
			if user is not None:
				login(request, user)
				if not user.role:
					return redirect("select_role")
				if user.role == "client" and not hasattr(user, "clientprofile"):
					return redirect("client_onboarding")
				if user.role == "advocate" and not hasattr(user, "advocateprofile"):
					return redirect("advocate_onboarding")
				return redirect("dashboard")

			form.add_error(None, "Invalid credentials.")
	else:
		form = LoginForm()

	return render(request, "form.html", {"form": form, "title": "Login"})


@login_required
def logout_view(request):
	logout(request)
	return redirect("landing")


def _needs_role_selection(user):
	return user.is_authenticated and not user.role


def _needs_onboarding(user):
	if not user.is_authenticated or not user.role:
		return False
	if user.role == "client":
		return not hasattr(user, "clientprofile")
	if user.role == "advocate":
		return not hasattr(user, "advocateprofile")
	return True


@login_required
def select_role(request):
	if request.user.role:
		return redirect("dashboard")

	if request.method == "POST":
		selected_role = request.POST.get("role")
		if selected_role in ["client", "advocate"]:
			request.user.role = selected_role
			request.user.save(update_fields=["role"])
			if selected_role == "client":
				return redirect("client_onboarding")
			return redirect("advocate_onboarding")
		messages.error(request, "Please select a valid role.")

	return render(request, "select_role.html")


@login_required
def client_onboarding(request):
	if _needs_role_selection(request.user):
		return redirect("select_role")
	if request.user.role != "client":
		return redirect("dashboard")
	if hasattr(request.user, "clientprofile"):
		return redirect("dashboard")

	if request.method == "POST":
		form = ClientProfileForm(request.POST, request.FILES, user=request.user)
		if form.is_valid():
			form.save(user=request.user)
			return redirect("dashboard")
	else:
		form = ClientProfileForm(user=request.user)

	return render(request, "client_onboarding.html", {"form": form, "title": "Client Onboarding"})


@login_required
def advocate_onboarding(request):
	if _needs_role_selection(request.user):
		return redirect("select_role")
	if request.user.role != "advocate":
		return redirect("dashboard")
	if hasattr(request.user, "advocateprofile"):
		return redirect("dashboard")

	if request.method == "POST":
		form = AdvocateProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user = request.user
			profile.save()
			return redirect("dashboard")
	else:
		form = AdvocateProfileForm()

	return render(request, "form.html", {"form": form, "title": "Advocate Onboarding"})


@login_required
def create_case(request):
	if _needs_role_selection(request.user):
		return redirect("select_role")
	if _needs_onboarding(request.user):
		if request.user.role == "client":
			return redirect("client_onboarding")
		return redirect("advocate_onboarding")
	if request.user.role != "client":
		messages.error(request, "Only clients can create cases.")
		return redirect("dashboard")

	client_profile = request.user.clientprofile
	if request.method == "POST":
		form = CaseForm(request.POST)
		if form.is_valid():
			case = form.save(commit=False)
			case.client = client_profile
			case.save()
			messages.success(request, "Case created successfully.")
			return redirect("dashboard")
	else:
		form = CaseForm()

	form.fields["advocate"].queryset = AdvocateProfile.objects.all().order_by("user__email")

	return render(request, "form.html", {"form": form, "title": "Add Case"})


@login_required
def update_case(request, case_id):
	if _needs_role_selection(request.user):
		return redirect("select_role")
	if _needs_onboarding(request.user):
		if request.user.role == "client":
			return redirect("client_onboarding")
		return redirect("advocate_onboarding")
	if request.user.role != "client":
		messages.error(request, "Only clients can update cases.")
		return redirect("dashboard")

	case = get_object_or_404(Case, id=case_id, client=request.user.clientprofile)

	if request.method == "POST":
		form = CaseForm(request.POST, instance=case)
		if form.is_valid():
			updated_case = form.save(commit=False)
			updated_case.client = request.user.clientprofile
			updated_case.save()
			messages.success(request, "Case updated successfully.")
			return redirect("dashboard")
	else:
		form = CaseForm(instance=case)

	form.fields["advocate"].queryset = AdvocateProfile.objects.all().order_by("user__email")
	return render(request, "form.html", {"form": form, "title": "Update Case"})


@login_required
def delete_case(request, case_id):
	if _needs_role_selection(request.user):
		return redirect("select_role")
	if _needs_onboarding(request.user):
		if request.user.role == "client":
			return redirect("client_onboarding")
		return redirect("advocate_onboarding")
	if request.user.role != "client":
		messages.error(request, "Only clients can delete cases.")
		return redirect("dashboard")

	case = get_object_or_404(Case, id=case_id, client=request.user.clientprofile)
	if request.method == "POST":
		case.delete()
		messages.success(request, "Case deleted successfully.")
		return redirect("dashboard")

	messages.error(request, "Invalid request for case deletion.")
	return redirect("dashboard")


@login_required
def create_hearing(request):
	if _needs_role_selection(request.user):
		return redirect("select_role")
	if _needs_onboarding(request.user):
		if request.user.role == "client":
			return redirect("client_onboarding")
		return redirect("advocate_onboarding")
	if request.user.role != "advocate":
		messages.error(request, "Only advocates can update hearings.")
		return redirect("dashboard")

	advocate_profile = request.user.advocateprofile
	if request.method == "POST":
		form = HearingForm(request.POST)
		if form.is_valid():
			hearing = form.save(commit=False)
			if hearing.case.advocate_id != advocate_profile.id:
				messages.error(request, "You can only update hearings for your assigned cases.")
			else:
				hearing.save()
				messages.success(request, "Hearing updated successfully.")
				return redirect("dashboard")
	else:
		form = HearingForm()

	form.fields["case"].queryset = Case.objects.filter(advocate=advocate_profile).order_by("-filing_date")

	return render(request, "form.html", {"form": form, "title": "Add Hearing"})


@login_required
def upload_document(request):
	if _needs_role_selection(request.user):
		return redirect("select_role")
	if _needs_onboarding(request.user):
		if request.user.role == "client":
			return redirect("client_onboarding")
		return redirect("advocate_onboarding")
	if request.user.role != "advocate":
		messages.error(request, "Only advocates can upload case documents.")
		return redirect("dashboard")

	advocate_profile = request.user.advocateprofile
	if request.method == "POST":
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			document = form.save(commit=False)
			if document.case.advocate_id != advocate_profile.id:
				messages.error(request, "You can only upload documents for your assigned cases.")
			else:
				document.save()
				messages.success(request, "Document uploaded successfully.")
				return redirect("dashboard")
	else:
		form = DocumentForm()

	form.fields["case"].queryset = Case.objects.filter(advocate=advocate_profile).order_by("-filing_date")

	return render(request, "form.html", {"form": form, "title": "Upload Document"})


@login_required
def create_task(request):
	if _needs_role_selection(request.user):
		return redirect("select_role")
	if _needs_onboarding(request.user):
		if request.user.role == "client":
			return redirect("client_onboarding")
		return redirect("advocate_onboarding")
	if request.user.role != "client":
		messages.error(request, "Only clients can create tasks.")
		return redirect("dashboard")

	client_profile = request.user.clientprofile
	if request.method == "POST":
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			if task.case.client_id != client_profile.id:
				messages.error(request, "You can only create tasks for your own cases.")
			else:
				task.save()
				messages.success(request, "Task created successfully.")
				return redirect("dashboard")
	else:
		form = TaskForm()

	form.fields["case"].queryset = Case.objects.filter(client=client_profile).order_by("-filing_date")

	return render(request, "form.html", {"form": form, "title": "Add Task"})


@login_required
def dashboard(request):
	if _needs_role_selection(request.user):
		return redirect("select_role")
	if _needs_onboarding(request.user):
		if request.user.role == "client":
			return redirect("client_onboarding")
		return redirect("advocate_onboarding")

	today = timezone.localdate()

	if request.user.role == "client":
		profile = request.user.clientprofile
		cases = Case.objects.filter(client=profile).order_by("-filing_date")
		upcoming_hearings = Hearing.objects.filter(case__client=profile, hearing_date__gte=today).order_by("hearing_date")
		tasks = Task.objects.filter(case__client=profile).order_by("due_date")
		context = {
			"role": "client",
			"cases": cases,
			"hearings": upcoming_hearings,
			"tasks": tasks,
		}
	else:
		profile = request.user.advocateprofile
		cases = Case.objects.filter(advocate=profile).order_by("-filing_date")
		hearings = Hearing.objects.filter(case__advocate=profile).order_by("hearing_date")
		documents = Document.objects.filter(case__advocate=profile).order_by("-uploaded_at")
		context = {
			"role": "advocate",
			"cases": cases,
			"hearings": hearings,
			"documents": documents,
		}

	return render(request, "dashboard.html", context)


@login_required
def case_detail(request, case_id):
	case = get_object_or_404(Case, id=case_id)
	if request.user.role == "client":
		if not hasattr(request.user, "clientprofile") or case.client_id != request.user.clientprofile.id:
			messages.error(request, "You do not have access to this case.")
			return redirect("dashboard")
	elif request.user.role == "advocate":
		if not hasattr(request.user, "advocateprofile") or case.advocate_id != request.user.advocateprofile.id:
			messages.error(request, "You do not have access to this case.")
			return redirect("dashboard")
	else:
		return redirect("select_role")

	return render(request, "case_detail.html", {"case": case})


@login_required
def download_case_pdf(request, case_id):
	case = get_object_or_404(Case, id=case_id)

	if request.user.role == "client":
		if not hasattr(request.user, "clientprofile") or case.client_id != request.user.clientprofile.id:
			return HttpResponseForbidden("You are not authorized to download this case report.")
	elif request.user.role == "advocate":
		if not hasattr(request.user, "advocateprofile") or case.advocate_id != request.user.advocateprofile.id:
			return HttpResponseForbidden("You are not authorized to download this case report.")
	else:
		return HttpResponseForbidden("You are not authorized to download this case report.")

	buffer = BytesIO()
	doc = SimpleDocTemplate(buffer)
	styles = getSampleStyleSheet()
	story = []

	client_user = case.client.user
	advocate_user = case.advocate.user
	today = timezone.localdate().strftime("%d %b %Y")

	story.append(Paragraph("Case Summary Report", styles["Title"]))
	story.append(Paragraph("Legal Portal", styles["Heading3"]))
	story.append(Paragraph(f"Date: {today}", styles["Normal"]))
	story.append(Spacer(1, 16))

	story.append(Paragraph("Client Details", styles["Heading2"]))
	story.append(Paragraph(f"Full Name: {client_user.get_full_name() or client_user.email}", styles["Normal"]))
	story.append(Paragraph(f"Phone: {client_user.phone or 'N/A'}", styles["Normal"]))
	story.append(Paragraph(f"Email: {client_user.email}", styles["Normal"]))
	story.append(Paragraph(f"Address: {case.client.address}", styles["Normal"]))
	story.append(Spacer(1, 12))

	story.append(Paragraph("Advocate Details", styles["Heading2"]))
	story.append(Paragraph(f"Full Name: {advocate_user.get_full_name() or advocate_user.email}", styles["Normal"]))
	story.append(Paragraph(f"Enrollment Number: {case.advocate.enrollment_number}", styles["Normal"]))
	story.append(Paragraph(f"Specialization: {case.advocate.specialization}", styles["Normal"]))
	story.append(Paragraph(f"Contact: {advocate_user.phone or 'N/A'}", styles["Normal"]))
	story.append(Spacer(1, 12))

	story.append(Paragraph("Case Details", styles["Heading2"]))
	story.append(Paragraph(f"Case Title: {case.title}", styles["Normal"]))
	story.append(Paragraph(f"Case Number: {case.case_number}", styles["Normal"]))
	story.append(Paragraph(f"Case Type: {case.case_type.title()}", styles["Normal"]))
	story.append(Paragraph(f"Court Name: {case.court_name}", styles["Normal"]))
	story.append(Paragraph(f"Filing Date: {case.filing_date}", styles["Normal"]))
	story.append(Paragraph(f"Status: {case.status.title()}", styles["Normal"]))
	story.append(Paragraph(f"Stage: {case.stage.title()}", styles["Normal"]))
	story.append(Spacer(1, 12))

	story.append(Paragraph("Description", styles["Heading2"]))
	story.append(Paragraph(case.description or "N/A", styles["Normal"]))

	doc.build(story)
	buffer.seek(0)

	safe_case_number = str(case.case_number).replace(" ", "_").replace("/", "_")
	response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
	response["Content-Disposition"] = f'attachment; filename="case_{safe_case_number}.pdf"'
	return response
