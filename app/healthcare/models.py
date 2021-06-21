import time
from django.db import models
from django.contrib.auth import get_user_model
from core.models import (
    University, Degree, Designation, SubDiscipline
)
from location.models import Location
from core.utils import get_unique_slug


def user_directory_path(instance, filename):
    name = str(int(time.time()))+'.'+filename.split('.')[-1]
    return 'user_{0}/{1}'.format(instance.user.id, name)


def organization_directory_path(instance, filename):
    name = str(int(time.time()))+'.'+filename.split('.')[-1]
    return 'org_{0}/{1}'.format(instance.id, name)


QUESTION_TYPES = (
    ('D', 'Description'),
    ('O', 'Option'),
)
ACTIVE = 'A'
INACTIVE = 'I'
APPROVED = 'A'
UNAPPROVED = 'U'
STATUS = (
    (ACTIVE, 'Active'),
    (INACTIVE, 'Inactive'),
)
GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)
APPROVAL_STATUS = (
    (APPROVED, 'Approved'),
    (UNAPPROVED, 'Unapproved'),
)


class DoctorProfile(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT
    )
    discipline = models.ForeignKey(
        SubDiscipline,
        on_delete=models.PROTECT
    )
    first_name = models.CharField(
        max_length=255
    )
    middle_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=255
    )
    permanent_address = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    profile_pic = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True
    )
    approval_status = models.CharField(
        max_length=2,
        choices=APPROVAL_STATUS,
        default=UNAPPROVED,
        null=True
    )

    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        name = self.first_name + ' '
        if self.middle_name:
            name += self.middle_name + ' '
        return name + ' ' + self.last_name + ' - ' + self.user.phone_number


class DoctorDegree(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.doctor

    class Meta:
        unique_together = ('doctor', 'degree', 'university')


class Organization(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    image = models.ImageField(
        upload_to=organization_directory_path,
        blank=True,
        null=True
    )
    remark = models.TextField(blank=True, null=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)


class DoctorVistingSchedules(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.PROTECT
    )
    date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField()
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT
    )
    remark = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'date', 'organization', 'in_time', 'out_time')


class PatientProfile(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT
    )
    first_name = models.CharField(
        max_length=255
    )
    middle_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=255
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER
    )
    date_of_birth = models.DateField(
        null=True
    )
    permanent_address = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    profile_pic = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True
    )
    approval_status = models.CharField(
        max_length=2,
        choices=APPROVAL_STATUS,
        default=UNAPPROVED,
    )
    remark = models.TextField(blank=True, null=True)
    registered_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        null=True,
        related_name='registered_by'
    )

    def __str__(self):
        name = self.first_name + ' '
        if self.middle_name:
            name += self.middle_name + ' '
        return name + ' ' + self.last_name + ' - ' + self.user.phone_number


class QuestionChoices(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question = models.CharField(
        max_length=255,
        unique=True
    )
    question_type = models.CharField(
        max_length=1,
        choices=QUESTION_TYPES
    )
    question_choices = models.ManyToManyField(
        QuestionChoices,
        blank=True,
    )

    def __str__(self):
        return self.question


class ConsellingQuestionSets(models.Model):
    name = models.CharField(max_length=255)
    question = models.ManyToManyField(
        Question
    )

    def __str__(self):
        return self.name


class ConsellingQuestionSetsAnswers(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    answer_description = models.TextField(null=True)
    answer_choice = models.ForeignKey(
        QuestionChoices,
        null=True,
        on_delete=models.CASCADE
    )


class PatientConsellingQuestionResult(models.Model):
    question_set = models.ForeignKey(
        ConsellingQuestionSets,
        on_delete=models.PROTECT
    )
    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.PROTECT
    )
    result = models.ManyToManyField(ConsellingQuestionSetsAnswers)
    finding = models.TextField(null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    appointment = models.ForeignKey(
        DoctorVistingSchedules,
        on_delete=models.PROTECT,
        null=True
    )
    assigned_date = models.DateTimeField(
        auto_now=True
    )
    approved_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    approved_date = models.DateTimeField(
        null=True,
        blank=True
    )
    approval_status = models.CharField(
        max_length=2,
        choices=APPROVAL_STATUS,
        default=UNAPPROVED,
    )

    class Meta:
        unique_together = ('question_set', 'patient', 'assigned_date')


class LabTestItems(models.Model):
    name = models.CharField(max_length=255, unique=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class LabTests(models.Model):
    name = models.CharField(max_length=255)
    items = models.ManyToManyField(
        LabTestItems
    )
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    home_service = models.BooleanField(default=False)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)


class Labs(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        allow_unicode=True
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT
    )
    tests = models.ManyToManyField(
        LabTests
    )
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, 'name', 'slug')
        super().save(*args, **kwargs)


class LabAgentProfile(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    lab = models.ForeignKey(
        Labs,
        on_delete=models.PROTECT
    )
    designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT
    )
    first_name = models.CharField(
        max_length=255
    )
    middle_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=255
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER
    )
    date_of_birth = models.DateField(
        null=True
    )
    permanent_address = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    profile_pic = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=ACTIVE,
    )
    remark = models.TextField(blank=True, null=True)
    registered_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        null=True,
        related_name='labagent_registered_by'
    )

    def __str__(self):
        return self.user.phone_number


class PatientLabTest(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.PROTECT)
    lab = models.ForeignKey(Labs, on_delete=models.PROTECT)
    test = models.ForeignKey(LabTests, on_delete=models.PROTECT)
    assigned_date = models.DateTimeField(auto_now=True)
    assigned_by = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    lab_agent = models.ForeignKey(
        LabAgentProfile, on_delete=models.PROTECT,
        null=True, blank=True
    )
    home_service = models.BooleanField(default=False)
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT,
        null=True, blank=True
    )
    address_detail = models.TextField(null=True, blank=True)
    remark = models.TextField(null=True,  blank=True)
    requested_date = models.DateTimeField()
    delivered_date = models.DateTimeField(null=True, blank=True)
    delivery_code = models.CharField(max_length=255, null=True, blank=True)


class PatientLabTestResult(models.Model):
    lab_test = models.ForeignKey(PatientLabTest, on_delete=models.CASCADE)
    test_items = models.ForeignKey(LabTestItems, on_delete=models.PROTECT)
    test_results = models.CharField(max_length=255)
