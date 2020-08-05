# Generated by Django 3.0.8 on 2020-08-04 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=255)),
                ('answer', models.CharField(blank=True, choices=[('Basic', 'Basic'), ('Good', 'Good'), ('Not Applicable', 'Not Applicable'), ('Not Assessed', 'Not Assessed'), ('Unsatisfactory', 'Unsatisfactory')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAdder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='Update Inspection', max_length=255)),
                ('question_text', models.CharField(blank=True, max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='StepStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('state_machine', models.CharField(max_length=255)),
                ('execution_arn', models.CharField(max_length=255)),
                ('current_status', models.CharField(default='None', max_length=255)),
                ('assignee', models.CharField(default='Not Assigned', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Warnings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposed_enforcement_action', models.CharField(choices=[('Composition Fine', 'Composition Fine'), ('Warning', 'Warning'), ('Notice', 'Notice')], max_length=20)),
                ('Act', models.CharField(max_length=255)),
                ('Law', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('stepStatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_process.StepStatus')),
            ],
        ),
        migrations.CreateModel(
            name='Update_Inspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Inspection_Category', models.CharField(max_length=100)),
                ('Inspection_Type', models.CharField(max_length=100)),
                ('Reference', models.CharField(choices=[('Case Management & Investigation', 'Case Management & Investigation'), ('Feedback and Appeal', 'Feedback and Appeal'), ('Incident Reporting', 'Incident Reporting'), ('Inspection & Engagement', 'Inspection & Engagement'), ('Monitoring and Surveillance', 'Monitoring and Surveillance')], max_length=100)),
                ('Reference_No', models.CharField(max_length=100)),
                ('Arrival_Date', models.DateTimeField(default=django.utils.timezone.now)),
                ('Arrival_Time', models.DateTimeField(default=django.utils.timezone.now)),
                ('Workplace_No', models.CharField(max_length=100)),
                ('stepStatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_process.StepStatus')),
            ],
        ),
        migrations.CreateModel(
            name='SWO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('justification', models.CharField(max_length=255)),
                ('offenderDetails', models.CharField(max_length=255)),
                ('stepStatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_process.StepStatus')),
            ],
        ),
        migrations.CreateModel(
            name='Questionaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('question', models.ManyToManyField(blank=True, to='the_process.Question')),
                ('stepStatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_process.StepStatus')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='questionAdder',
            field=models.ForeignKey(blank=True, max_length=200, on_delete=django.db.models.deletion.CASCADE, to='the_process.QuestionAdder'),
        ),
        migrations.AddField(
            model_name='question',
            name='stepStatus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_process.StepStatus'),
        ),
        migrations.CreateModel(
            name='HistoricalStepStatus',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('state_machine', models.CharField(max_length=255)),
                ('execution_arn', models.CharField(max_length=255)),
                ('current_status', models.CharField(default='None', max_length=255)),
                ('assignee', models.CharField(default='Not Assigned', max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical step status',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Findings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Section_A', models.CharField(max_length=255)),
                ('Document_Name', models.CharField(max_length=255)),
                ('Document_type', models.CharField(choices=[('Documents and Photos', 'Documents and Photos'), ('Photos', 'Photos'), ('Supporting Documents', 'Supporting Documents')], max_length=255)),
                ('Section_of_Group', models.CharField(choices=[('Section(A) - 1', 'Section(A) - 1')], max_length=20)),
                ('Description_A', models.CharField(max_length=255)),
                ('finished', models.CharField(blank=True, max_length=255)),
                ('stepStatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_process.StepStatus')),
            ],
        ),
        migrations.CreateModel(
            name='ApproveOfficer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.CharField(choices=[('Approve', 'Approve'), ('Reassign', 'Reassign')], max_length=255)),
                ('stepStatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_process.StepStatus')),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.CharField(choices=[('Approve', 'Approve'), ('Clarifications', 'Clarifications'), ('Reassign', 'Reassign')], max_length=255)),
                ('remarks', models.CharField(max_length=255)),
                ('stepStatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='the_process.StepStatus')),
            ],
        ),
    ]
