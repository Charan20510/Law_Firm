from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import AdvocateProfile, Case, ClientProfile, Document, Hearing, Task

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import AdvocateProfile, Case, ClientProfile, Document, Hearing, Task

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter email address"}),
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"placeholder": "Enter password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm password"})


class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Enter email address"}),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}),
    )


class ClientProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        label="First Name *",
        widget=forms.TextInput(attrs={"placeholder": "Enter first name"}),
    )
    last_name = forms.CharField(
        required=True,
        label="Last Name *",
        widget=forms.TextInput(attrs={"placeholder": "Enter last name"}),
    )
    email = forms.EmailField(
        required=True,
        label="Email *",
        widget=forms.EmailInput(attrs={"placeholder": "Enter email address"}),
    )
    mobile_number = forms.CharField(
        required=True,
        label="Mobile Number *",
        widget=forms.TextInput(attrs={"placeholder": "Enter 10-digit mobile number"}),
    )
    flat_house_no = forms.CharField(
        required=True,
        label="Flat / House No *",
        widget=forms.TextInput(attrs={"placeholder": "Flat / House No / Building"}),
    )
    area_street = forms.CharField(
        required=True,
        label="Area / Street *",
        widget=forms.TextInput(attrs={"placeholder": "Area, Street, Sector"}),
    )
    landmark = forms.CharField(
        required=False,
        label="Landmark",
        widget=forms.TextInput(attrs={"placeholder": "Near hospital, school, etc."}),
    )
    city = forms.CharField(
        required=True,
        label="City *",
        widget=forms.TextInput(attrs={"placeholder": "Enter city"}),
    )
    state = forms.ChoiceField(
        required=True,
        label="State *",
        choices=[
            ("", "Select state"),
            ("Andhra Pradesh", "Andhra Pradesh"),
            ("Bihar", "Bihar"),
            ("Delhi", "Delhi"),
            ("Gujarat", "Gujarat"),
            ("Karnataka", "Karnataka"),
            ("Maharashtra", "Maharashtra"),
            ("Rajasthan", "Rajasthan"),
            ("Tamil Nadu", "Tamil Nadu"),
            ("Telangana", "Telangana"),
            ("Uttar Pradesh", "Uttar Pradesh"),
            ("West Bengal", "West Bengal"),
        ],
    )
    pincode = forms.CharField(
        required=True,
        label="Pincode *",
        widget=forms.TextInput(attrs={"placeholder": "6-digit PIN code"}),
    )

    class Meta:
        model = ClientProfile
        fields = [
            "father_name",
            "dob",
            "gender",
            "aadhaar",
            "pan",
            "photo",
            "id_proof",
            "signature",
        ]
        widgets = {
            "father_name": forms.TextInput(attrs={"placeholder": "Enter father name"}),
            "dob": forms.DateInput(attrs={"type": "date"}),
            "gender": forms.Select(
                choices=[("", "Select gender"), ("male", "Male"), ("female", "Female"), ("other", "Other")]
            ),
            "aadhaar": forms.TextInput(attrs={"placeholder": "XXXX-XXXX-XXXX"}),
            "pan": forms.TextInput(attrs={"placeholder": "ABCDE1234F"}),
            "photo": forms.ClearableFileInput(),
            "id_proof": forms.ClearableFileInput(),
            "signature": forms.ClearableFileInput(),
        }
        labels = {
            "father_name": "Father Name *",
            "dob": "Date of Birth *",
            "gender": "Gender *",
            "aadhaar": "Aadhaar Number *",
            "pan": "PAN Number *",
            "photo": "Photo *",
            "id_proof": "ID Proof *",
            "signature": "Signature *",
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            self.fields["email"].initial = self.user.email
            self.fields["mobile_number"].initial = self.user.phone

        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} onboarding-input".strip()

    def clean_mobile_number(self):
        mobile = self.cleaned_data["mobile_number"].strip()
        digits = "".join(ch for ch in mobile if ch.isdigit())
        if len(digits) != 10:
            raise ValidationError("Mobile number must be exactly 10 digits.")
        return digits

    def clean_pincode(self):
        pincode = self.cleaned_data["pincode"].strip()
        if not (pincode.isdigit() and len(pincode) == 6):
            raise ValidationError("Pincode must be exactly 6 digits.")
        return pincode

    def save(self, commit=True, user=None):
        profile = super().save(commit=False)
        target_user = user or self.user

        flat_house_no = self.cleaned_data["flat_house_no"].strip()
        area_street = self.cleaned_data["area_street"].strip()
        landmark = self.cleaned_data.get("landmark", "").strip()
        city = self.cleaned_data["city"].strip()
        state = self.cleaned_data["state"]
        pincode = self.cleaned_data["pincode"].strip()

        structured_address = [
            f"Flat/House No: {flat_house_no}",
            f"Area/Street: {area_street}",
            f"Landmark: {landmark or 'N/A'}",
            f"City: {city}",
            f"State: {state}",
            f"Pincode: {pincode}",
        ]
        profile.address = "\n".join(structured_address)

        if target_user is not None:
            target_user.first_name = self.cleaned_data["first_name"].strip()
            target_user.last_name = self.cleaned_data["last_name"].strip()
            target_user.email = self.cleaned_data["email"].strip().lower()
            target_user.phone = self.cleaned_data["mobile_number"]
            if commit:
                target_user.save(update_fields=["first_name", "last_name", "email", "phone"])
            profile.user = target_user

        if commit:
            profile.save()
        return profile


class AdvocateProfileForm(forms.ModelForm):
    class Meta:
        model = AdvocateProfile
        fields = [
            "enrollment_number",
            "bar_council",
            "specialization",
            "experience_years",
            "office_address",
            "photo",
            "signature",
        ]
        widgets = {
            "enrollment_number": forms.TextInput(attrs={"placeholder": "Enter enrollment number"}),
            "bar_council": forms.TextInput(attrs={"placeholder": "Enter bar council"}),
            "specialization": forms.TextInput(attrs={"placeholder": "Enter specialization"}),
            "experience_years": forms.NumberInput(attrs={"placeholder": "Enter years of experience"}),
            "office_address": forms.Textarea(attrs={"rows": 3, "placeholder": "Enter office address"}),
        }


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [
            "title",
            "case_number",
            "case_type",
            "court_name",
            "advocate",
            "opponent_details",
            "filing_date",
            "status",
            "stage",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter case title"}),
            "case_number": forms.TextInput(attrs={"placeholder": "Enter case number"}),
            "court_name": forms.TextInput(attrs={"placeholder": "Enter court name"}),
            "opponent_details": forms.Textarea(attrs={"rows": 3, "placeholder": "Enter opponent details"}),
            "filing_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Enter case description"}),
        }


class HearingForm(forms.ModelForm):
    class Meta:
        model = Hearing
        fields = [
            "case",
            "hearing_date",
            "next_hearing_date",
            "notes",
            "judge_remarks",
            "status",
        ]
        widgets = {
            "hearing_date": forms.DateInput(attrs={"type": "date"}),
            "next_hearing_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Enter hearing notes"}),
            "judge_remarks": forms.Textarea(attrs={"rows": 3, "placeholder": "Enter judge remarks"}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["case", "file", "document_type", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3, "placeholder": "Enter document notes"}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "case", "due_date", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Enter task title"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }
