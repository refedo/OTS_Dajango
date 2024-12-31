from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_number', models.CharField(max_length=10, unique=True, verbose_name='Project #', help_text='Simple project number (e.g., 1001)')),
                ('name', models.CharField(max_length=255, verbose_name='Project Name')),
                ('client_name', models.CharField(max_length=100, verbose_name='Client Name')),
                ('status', models.CharField(choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('on_hold', 'On Hold')], default='not_started', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['project_number'],
            },
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Building A', max_length=100, help_text='Building name (e.g., "Building A", "Building B")')),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buildings', to='core.project')),
            ],
            options={
                'verbose_name': 'Building',
                'verbose_name_plural': 'Buildings',
                'ordering': ['project', 'name'],
                'unique_together': {('project', 'name')},
            },
        ),
    ]