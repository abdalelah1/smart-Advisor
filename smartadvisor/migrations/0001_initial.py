# Generated by Django 4.0.4 on 2023-10-20 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=20)),
                ('credit', models.CharField(max_length=10)),
                ('is_reuqired', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeOfCourse', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('full_courses_count', models.IntegerField()),
                ('no_hourse_Tobe_graduated', models.IntegerField()),
                ('no_required_Elecvtive', models.IntegerField()),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.college')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('no_university_courses_required', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='University_Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=20)),
                ('credit', models.CharField(max_length=10)),
                ('is_reuqired', models.BooleanField(default=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.level')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university_ID', models.CharField(max_length=50)),
                ('GPA', models.CharField(max_length=50)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.level')),
            ],
        ),
        migrations.CreateModel(
            name='Recommended_Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_student', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.student')),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.department')),
            ],
        ),
        migrations.CreateModel(
            name='Course_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree', models.CharField(max_length=50)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.student')),
                ('universit_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.university_courses')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.level'),
        ),
        migrations.AddField(
            model_name='course',
            name='major',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.major'),
        ),
        migrations.AddField(
            model_name='course',
            name='preRequst',
            field=models.ManyToManyField(to='smartadvisor.course'),
        ),
        migrations.AddField(
            model_name='course',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.course_type'),
        ),
        migrations.AddField(
            model_name='college',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.university'),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartadvisor.college')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
