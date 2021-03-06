# Generated by Django 3.0.8 on 2020-09-28 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_guest', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=1200)),
                ('online', models.BooleanField(default=False)),
                ('channel_name', models.CharField(max_length=255, null=True)),
                ('friends', models.ManyToManyField(related_name='_user_friends_+', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('group_channel_name', models.CharField(max_length=512)),
                ('date_played', models.DateField(auto_now_add=True)),
                ('_status', models.CharField(choices=[('stalemate', 'Stalemate'), ('checkmate', 'Checkmate'), ('in_progress', 'In Progress'), ('resign', 'Resign'), ('timeout', 'Timeout')], default='in_progress', max_length=32)),
                ('_started', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DecimalField(decimal_places=2, default=60.0, max_digits=6)),
                ('_turn', models.BooleanField(default=False)),
                ('colour', models.BooleanField()),
                ('winner', models.BooleanField(default=False)),
                ('draw', models.BooleanField(default=False)),
                ('turn_started_timestamp', models.DecimalField(decimal_places=2, max_digits=14, null=True)),
                ('resigned', models.BooleanField(default=False)),
                ('timeout', models.BooleanField(default=False)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_to_user', to='core.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_to_game', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('move_number', models.IntegerField()),
                ('colour', models.BooleanField()),
                ('piece_type', models.CharField(choices=[('R', 'Rook'), ('N', 'Knight'), ('B', 'Bishop'), ('K', 'King'), ('Q', 'Queen'), ('p', 'Pawn')], max_length=32)),
                ('captured_piece_type', models.CharField(choices=[('R', 'Rook'), ('N', 'Knight'), ('B', 'Bishop'), ('K', 'King'), ('Q', 'Queen'), ('p', 'Pawn')], max_length=32, null=True)),
                ('from_position_x', models.IntegerField()),
                ('from_position_y', models.IntegerField()),
                ('to_position_x', models.IntegerField()),
                ('to_position_y', models.IntegerField()),
                ('move_type', models.CharField(choices=[('castle', 'Castle'), ('en_passant', 'En Passant'), ('regular', 'Regular')], max_length=32)),
                ('notation', models.CharField(max_length=10)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moves', to='core.Game')),
            ],
        ),
        migrations.CreateModel(
            name='GameInvite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('game_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('message', models.CharField(max_length=255)),
                ('_accepted', models.BooleanField(default=False)),
                ('_declined', models.BooleanField(default=False)),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invite_from', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invite_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(through='core.Player', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=4096)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='core.Game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
