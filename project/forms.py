from django import forms
from django.core.exceptions import ValidationError
from .models import Project, Tag, ProjectPicture

class ProjectForm(forms.ModelForm):
    tags = forms.CharField(max_length=100, required=True, help_text='Enter tags separated by commas')
    images = forms.FileField(required=True, label='Project Images')
    start_time = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), input_formats=('%Y-%m-%d',))
    end_time = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), input_formats=('%Y-%m-%d',))

    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time', 'country']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.replace(' ', '')) < 3:
            raise ValidationError("Title must be at least 3 characters long.")
        if not title.replace(' ', '').isalnum() or not any(char.isalpha() for char in title):
            raise ValidationError("Title must contain letters or letters with numbers.")
        return title

    def clean_details(self):
        details = self.cleaned_data.get('details')
        if len(details.replace(' ', '')) < 10:
            raise ValidationError("Details must be at least 10 characters long.")
        if not details.replace(' ', '').isalnum() or not any(char.isalpha() for char in details):
            raise ValidationError("Details must contain letters or letters with numbers.")
        return details

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country is None:
            raise ValidationError("Country is required.")
        if not country.replace(' ', '').isalpha():
            raise ValidationError("Country must contain letters only.")
        return country
   


    def save(self, creator):
        project = super().save(commit=False)
        project.creator = creator
        project.save()

        tags = self.cleaned_data.get('tags')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            for tag in tag_list:
                tag_obj, _ = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag_obj)

        images = self.files.getlist('images')
        for image in images:
            ProjectPicture.objects.create(project=project, image=image)

        return project