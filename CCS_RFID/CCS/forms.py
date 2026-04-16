from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import RegexValidator  # ADD THIS
from .models import User

class AdminLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full py-[11px] pl-[38px] pr-10 border-[1.5px] border-[#e0dbd4] rounded-lg font-dmsans text-[14px]',
            'placeholder': 'Enter your email',
            'id': 'emailInput'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full py-[11px] pl-[38px] pr-10 border-[1.5px] border-[#e0dbd4] rounded-lg font-dmsans text-[14px]',
            'placeholder': 'Enter your password',
            'id': 'passwordInput'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'password']

class StudentLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full py-[11px] pl-[38px] pr-10 border-[1.5px] border-[#e0dbd4] rounded-lg font-dmsans text-[14px]',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full py-[11px] pl-[38px] pr-10 border-[1.5px] border-[#e0dbd4] rounded-lg font-dmsans text-[14px]',
            'placeholder': 'Enter your password'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'password']

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
            'placeholder': 'Create a password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
            'placeholder': 'Re-enter password'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'first_name', 'middle_name', 'last_name', 'email',
            'date_of_birth', 'gender', 'civil_status',
            'contact_person', 'contact_number', 'college', 
            'department', 'course'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'First Name',
                'id': 'firstName'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'Middle Name',
                'id': 'middleName'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'Last Name',
                'id': 'lastName'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'Email Address',
                'id': 'email'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'id': 'dateOfBirth'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg appearance-none',
                'id': 'gender'
            }),
            'civil_status': forms.Select(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg appearance-none',
                'id': 'civilStatus'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'Contact Person',
                'id': 'contactPerson'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'Contact Number',
                'id': 'contactNumber'
            }),
            'college': forms.Select(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg appearance-none',
                'id': 'college'
            }),
            'department': forms.Select(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg appearance-none',
                'id': 'department'
            }),
            'course': forms.Select(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg appearance-none',
                'id': 'course'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = 'admin'
        if commit:
            user.save()
        return user

class StudentRegistrationForm(forms.ModelForm):
    # ============================================
    # ADDED: Student ID field with validation
    # ============================================
    student_id = forms.CharField(
        max_length=10,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{4}-\d{5}$',
                message='Student ID must be in format: YYYY-XXXXX (e.g., 2022-00779)'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
            'placeholder': 'YYYY-XXXXX (e.g., 2022-00779)',
            'id': 'studentId'
        })
    )
    
    # ============================================
    # MODIFIED: Email field with domain validation
    # ============================================
    email = forms.EmailField(
        validators=[
            RegexValidator(
                regex=r'^[^\s@]+@wmsu\.edu\.ph$',
                message='Only @wmsu.edu.ph email addresses are allowed'
            )
        ],
        widget=forms.EmailInput(attrs={
            'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
            'placeholder': 'Email Address (@wmsu.edu.ph)',
            'id': 'email'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
            'placeholder': 'Create a password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
            'placeholder': 'Re-enter password'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'student_id',  # ADDED: Student ID field
            'first_name', 'middle_name', 'last_name', 'email',
            'date_of_birth', 'gender', 'civil_status',
            'contact_person', 'contact_number', 'college', 
            'department', 'course'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'First Name',
                'id': 'firstName'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'Middle Name',
                'id': 'middleName'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'Last Name',
                'id': 'lastName'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'id': 'dateOfBirth'
            }),
            'gender': forms.Select(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg appearance-none',
                'id': 'gender'
            }),
            'civil_status': forms.Select(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg appearance-none',
                'id': 'civilStatus'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'Contact Person',
                'id': 'contactPerson'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg',
                'placeholder': 'Contact Number',
                'id': 'contactNumber'
            }),
            'college': forms.Select(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg appearance-none',
                'id': 'college'
            }),
            'department': forms.Select(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg appearance-none',
                'id': 'department'
            }),
            'course': forms.Select(attrs={
                'class': 'w-full py-3 px-4 border-[1.5px] border-[#e0dbd4] rounded-lg appearance-none',
                'id': 'course'
            }),
        }
    
    def clean_student_id(self):
        """Validate Student ID is unique"""
        student_id = self.cleaned_data.get('student_id')
        if student_id:
            # Check if Student ID already exists
            if User.objects.filter(student_id=student_id).exists():
                raise forms.ValidationError("Student ID already exists. Please use a different Student ID.")
        return student_id
    
    def clean_email(self):
        """Validate Email is unique and has correct domain"""
        email = self.cleaned_data.get('email')
        if email:
            # Check if Email already exists
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists. Please use a different email address.")
            
            # Double-check domain (already validated by RegexValidator)
            if not email.lower().endswith('@wmsu.edu.ph'):
                raise forms.ValidationError("Only @wmsu.edu.ph email addresses are allowed")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data
    
    def save(self, commit=True):
        print("=" * 50)
        print("DEBUG: Inside save method")
        print(f"cleaned_data student_id: {self.cleaned_data.get('student_id')}")
        print(f"All cleaned_data: {self.cleaned_data}")
        print("=" * 50)
        
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.user_type = 'student'
        
        # Set the student_id from form data
        user.student_id = self.cleaned_data.get('student_id')
        print(f"user.student_id after assignment: {user.student_id}")
        print("=" * 50)
        
        if commit:
            user.save()
            print(f"✅ User saved with ID: {user.id}")
            print(f"✅ Student ID in database: {user.student_id}")
            print("=" * 50)
        
        return user