from django import forms
from django.utils.text import slugify
from .models import Task
from .models import Project, Contracts
from register.models import Company
from django.contrib.auth.models import User
from brownie import accounts, project, network, Contract
import json

# connecting and loading contract
mycontract = project.load()
contract_loadded = mycontract.ProjectContract
network_name = "ganache-local"  # Replace with the desired network name
network.connect(network_name)
explorer_url = "http://localhost:8545/"


status = (
    ('1', 'Stuck'),
    ('2', 'Working'),
    ('3', 'Done'),
)

due = (
    ('1', 'On Due'),
    ('2', 'Overdue'),
    ('3', 'Done'),
)


def get_account():
    return accounts.add("0x47640371453fe3c832709937ed6cbeb489a107d711ab26402e29121caad0e639")


class TaskRegistrationForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    task_name = forms.CharField(widget=forms.Textarea)
    status = forms.ChoiceField(choices=status)
    due = forms.ChoiceField(choices=due)
    file = forms.FileField(label="Select a file")

    class Meta:
        model = Task
        fields = '__all__'

    def save(self, commit=True):
        task = super(TaskRegistrationForm, self).save(commit=False)
        task.project = self.cleaned_data['project']
        task.task_name = self.cleaned_data['task_name']
        task.status = self.cleaned_data['status']
        task.due = self.cleaned_data['due']
        task.file = self.cleaned_data['file']
        task.save()
        assigns = self.cleaned_data['assign']
        for assign in assigns:
            task.assign.add((assign))

        if commit:
            with open("projects\ProjectContract.json", 'r') as file:
                json_data = json.load(file)
            abi = json_data["abi"]

            my_contract = Contracts.objects.get(name=task.project)
            contract_address = my_contract.address
            mycontract = Contract.from_abi(
                'ProjectContract', contract_address, abi)
            account = get_account()
            print(contract_address)
            transaction = mycontract.addTask(
                assign, task.task_name, {"from": account})
            transaction.wait(1)
            updated_people = mycontract.tasks(0)
            print(updated_people, "New VALUE")
            task.save()

        def clean_file(self):
            file = self.cleaned_data.get('file', False)
            if file:
                if file._size > 10 * 1024 * 1024:
                    raise forms.ValidationError(
                        "File size must be no more than 10 MB.")
            return file

        return task

    def __init__(self, *args, **kwargs):
        super(TaskRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['project'].widget.attrs['class'] = 'form-control'
        self.fields['project'].widget.attrs['placeholder'] = 'Social Name'
        self.fields['task_name'].widget.attrs['class'] = 'form-control'
        self.fields['task_name'].widget.attrs['placeholder'] = 'Name'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Email'
        self.fields['due'].widget.attrs['class'] = 'form-control'
        self.fields['due'].widget.attrs['placeholder'] = 'City'
        self.fields['assign'].widget.attrs['class'] = 'form-control'
        self.fields['assign'].widget.attrs['placeholder'] = 'Found date'
        self.fields['file'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['placeholder'] = 'Upload file'


class ProjectRegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=80)
    # slug = forms.SlugField('shortcut')
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    efforts = forms.DurationField()
    status = forms.ChoiceField(choices=status)
    dead_line = forms.DateField()
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    complete_per = forms.FloatField(min_value=0, max_value=100)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Project
        fields = '__all__'

    def save(self, commit=True):
        Project = super(ProjectRegistrationForm, self).save(commit=False)
        Project.name = self.cleaned_data['name']
        Project.efforts = self.cleaned_data['efforts']
        Project.status = self.cleaned_data['status']
        Project.dead_line = self.cleaned_data['dead_line']
        Project.company = self.cleaned_data['company']
        Project.complete_per = self.cleaned_data['complete_per']
        Project.description = self.cleaned_data['description']
        Project.slug = slugify(str(self.cleaned_data['name']))
        Project.save()
        assigns = self.cleaned_data['assign']
        for assign in assigns:
            Project.assign.add((assign))

        if commit:
            account = get_account()
            global contract
            contract = contract_loadded.deploy({"from": account})
            contract_address = contract.address
            data = Contracts(address=contract_address, name=Project.name)
            data.save()
            stored_value = contract.createProject(
                Project.name, "whole staff", 31425265, Project.description, {"from": account})
            print(stored_value, "OLD VALUE")

            Project.save()

        return Project

    def __init__(self, *args, **kwargs):
        super(ProjectRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Project Name'
        self.fields['efforts'].widget.attrs['class'] = 'form-control'
        self.fields['efforts'].widget.attrs['placeholder'] = 'Efforts'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Status'
        self.fields['dead_line'].widget.attrs['class'] = 'form-control'
        self.fields['dead_line'].widget.attrs['placeholder'] = 'Dead Line, type a date'
        self.fields['company'].widget.attrs['class'] = 'form-control'
        self.fields['company'].widget.attrs['placeholder'] = 'Company'
        self.fields['complete_per'].widget.attrs['class'] = 'form-control'
        self.fields['complete_per'].widget.attrs['placeholder'] = 'Complete %'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Type here the project description...'
        self.fields['assign'].widget.attrs['class'] = 'form-control'
