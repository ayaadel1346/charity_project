from django import forms
from .models import Project, Tag, ProjectPicture

class ProjectForm(forms.ModelForm):
    tags = forms.CharField(max_length=100, required=False, help_text='Enter tags separated by commas')
    images = forms.FileField(required=False, label='Project Images')
    start_time = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), input_formats=('%Y-%m-%d',))
    end_time = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), input_formats=('%Y-%m-%d',))

    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time', 'country']

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
