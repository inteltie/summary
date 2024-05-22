# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ActionItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    priority = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField()
    status = models.CharField(max_length=100)
    approved_by = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    assigned_to = models.ForeignKey('User', models.DO_NOTHING, related_name='actionitem_assigned_to_set', blank=True, null=True)
    meeting = models.ForeignKey('Meeting', models.DO_NOTHING)
    owner = models.ForeignKey('User', models.DO_NOTHING, related_name='actionitem_owner_set', blank=True, null=True)
    reporter = models.ForeignKey('User', models.DO_NOTHING, related_name='actionitem_reporter_set', blank=True, null=True)
    sustainable_action_item = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'action_item'


class ActionItemComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    actionitem = models.ForeignKey(ActionItem, models.DO_NOTHING)
    comment = models.ForeignKey('TaskComment', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'action_item_comment'
        unique_together = (('actionitem', 'comment'),)


class Announcement(models.Model):
    id = models.BigAutoField(primary_key=True)
    announcement_text = models.TextField()
    meeting = models.OneToOneField('Meeting', models.DO_NOTHING)
    transcript = models.OneToOneField('Transcript', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'announcement'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class Decision(models.Model):
    id = models.BigAutoField(primary_key=True)
    decision_text = models.TextField()
    meeting = models.OneToOneField('Meeting', models.DO_NOTHING)
    transcript = models.OneToOneField('Transcript', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'decision'


class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'department'


class Dependency(models.Model):
    id = models.BigAutoField(primary_key=True)
    dependency_text = models.TextField()
    meeting = models.OneToOneField('Meeting', models.DO_NOTHING)
    transcript = models.OneToOneField('Transcript', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'dependency'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryBeatClockedschedule(models.Model):
    clocked_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_clockedschedule'


class DjangoCeleryBeatCrontabschedule(models.Model):
    minute = models.CharField(max_length=240)
    hour = models.CharField(max_length=96)
    day_of_week = models.CharField(max_length=64)
    day_of_month = models.CharField(max_length=124)
    month_of_year = models.CharField(max_length=64)
    timezone = models.CharField(max_length=63)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_crontabschedule'


class DjangoCeleryBeatIntervalschedule(models.Model):
    every = models.IntegerField()
    period = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_intervalschedule'


class DjangoCeleryBeatPeriodictask(models.Model):
    name = models.CharField(unique=True, max_length=200)
    task = models.CharField(max_length=200)
    args = models.TextField()
    kwargs = models.TextField()
    queue = models.CharField(max_length=200, blank=True, null=True)
    exchange = models.CharField(max_length=200, blank=True, null=True)
    routing_key = models.CharField(max_length=200, blank=True, null=True)
    expires = models.DateTimeField(blank=True, null=True)
    enabled = models.IntegerField()
    last_run_at = models.DateTimeField(blank=True, null=True)
    total_run_count = models.PositiveIntegerField()
    date_changed = models.DateTimeField()
    description = models.TextField()
    crontab = models.ForeignKey(DjangoCeleryBeatCrontabschedule, models.DO_NOTHING, blank=True, null=True)
    interval = models.ForeignKey(DjangoCeleryBeatIntervalschedule, models.DO_NOTHING, blank=True, null=True)
    solar = models.ForeignKey('DjangoCeleryBeatSolarschedule', models.DO_NOTHING, blank=True, null=True)
    one_off = models.IntegerField()
    start_time = models.DateTimeField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    headers = models.TextField()
    clocked = models.ForeignKey(DjangoCeleryBeatClockedschedule, models.DO_NOTHING, blank=True, null=True)
    expire_seconds = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictask'


class DjangoCeleryBeatPeriodictasks(models.Model):
    ident = models.SmallIntegerField(primary_key=True)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_celery_beat_periodictasks'


class DjangoCeleryBeatSolarschedule(models.Model):
    event = models.CharField(max_length=24)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'django_celery_beat_solarschedule'
        unique_together = (('event', 'latitude', 'longitude'),)


class DjangoCeleryResultsChordcounter(models.Model):
    group_id = models.CharField(unique=True, max_length=255)
    sub_tasks = models.TextField()
    count = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'django_celery_results_chordcounter'


class DjangoCeleryResultsGroupresult(models.Model):
    group_id = models.CharField(unique=True, max_length=255)
    date_created = models.DateTimeField()
    date_done = models.DateTimeField()
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_groupresult'


class DjangoCeleryResultsTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    task_args = models.TextField(blank=True, null=True)
    task_kwargs = models.TextField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    worker = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField()
    periodic_task_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Keylabel(models.Model):
    id = models.BigAutoField(primary_key=True)
    keypoint_text = models.TextField()
    meeting = models.OneToOneField('Meeting', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'keylabel'


class Keypoint(models.Model):
    id = models.BigAutoField(primary_key=True)
    keypoint_text = models.TextField()
    meeting = models.OneToOneField('Meeting', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'keypoint'


class Meeting(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    nature = models.CharField(max_length=100, blank=True, null=True)
    schedule_date = models.DateField()
    schedule_time = models.TimeField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    type = models.CharField(max_length=200)
    channel = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    audio = models.CharField(max_length=100, blank=True, null=True)
    video = models.CharField(max_length=100, blank=True, null=True)
    department = models.ForeignKey(Department, models.DO_NOTHING)
    organization = models.ForeignKey('Organization', models.DO_NOTHING)
    organizer = models.ForeignKey('User', models.DO_NOTHING)
    audio_length = models.CharField(max_length=100, blank=True, null=True)
    is_delete = models.IntegerField()
    meeting_uuid = models.CharField(unique=True, max_length=32)
    platform = models.CharField(max_length=100)
    recurrent = models.IntegerField()
    status = models.CharField(max_length=9)
    duration = models.CharField(max_length=100, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    mic_audio = models.CharField(max_length=100, blank=True, null=True)
    speaker_video = models.CharField(max_length=100, blank=True, null=True)
    meeting_platform_id = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meeting'


class MeetingAgendaAttachment(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.CharField(max_length=100)
    meeting = models.ForeignKey(Meeting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meeting_agenda_attachment'


class MeetingAnalytics(models.Model):
    id = models.BigAutoField(primary_key=True)
    health = models.IntegerField()
    sustainable_index = models.IntegerField()
    participation_engagement = models.IntegerField()
    meeting_id = models.BigIntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'meeting_analytics'


class MeetingAttachment(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.CharField(max_length=100)
    meeting = models.ForeignKey(Meeting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meeting_attachment'


class MeetingFeedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    feedback = models.IntegerField()
    feedback_comment = models.TextField(blank=True, null=True)
    made_by = models.ForeignKey('User', models.DO_NOTHING)
    meeting = models.ForeignKey(Meeting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meeting_feedback'


class MeetingMeetingprocessing(models.Model):
    id = models.BigAutoField(primary_key=True)
    task_id = models.CharField(max_length=100)
    status = models.CharField(max_length=15)
    reason = models.CharField(max_length=200, blank=True, null=True)
    meeting = models.OneToOneField(Meeting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meeting_meetingprocessing'


class MeetingNotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment = models.TextField()
    created_at = models.DateTimeField()
    made_by = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    meeting = models.ForeignKey(Meeting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meeting_notes'


class MeetingNotification(models.Model):
    id = models.BigAutoField(primary_key=True)
    notification_id = models.CharField(max_length=500)
    error_message = models.TextField()
    meeting = models.OneToOneField(Meeting, models.DO_NOTHING)
    user_id = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'meeting_notification'


class MeetingSharingList(models.Model):
    id = models.BigAutoField(primary_key=True)
    meeting_id = models.ForeignKey(Meeting, models.DO_NOTHING)
    user_id = models.ForeignKey('User', models.DO_NOTHING)
    role = models.CharField(max_length=100)
    permission = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'meeting_sharing_list'
        unique_together = (('meeting_id', 'user_id'),)


class MeetingSqstracking(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.TextField()
    meeting = models.ForeignKey(Meeting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'meeting_sqstracking'


class Organization(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'organization'


class OrganizationadminJobtitle(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'organizationAdmin_jobtitle'


class Participant(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=9)
    meeting = models.ForeignKey(Meeting, models.DO_NOTHING)
    participant = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'participant'


class RecurringMeeting(models.Model):
    id = models.BigAutoField(primary_key=True)
    current_meeting = models.ForeignKey(Meeting, models.DO_NOTHING)
    previous_meeting = models.ForeignKey(Meeting, models.DO_NOTHING, related_name='recurringmeeting_previous_meeting_set')

    class Meta:
        managed = False
        db_table = 'recurring_meeting'


class Summary(models.Model):
    id = models.BigAutoField(primary_key=True)
    summary_text = models.TextField()
    summary_audio = models.CharField(max_length=250, blank=True, null=True)
    meeting = models.OneToOneField(Meeting, models.DO_NOTHING)
    transcript = models.OneToOneField('Transcript', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'summary'


class TaskAttachment(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.CharField(max_length=100)
    action = models.ForeignKey(ActionItem, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'task_attachment'


class TaskComment(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment = models.TextField()
    created_at = models.DateTimeField()
    made_by = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'task_comment'


class TokenBlacklistBlacklistedtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'


class Transcript(models.Model):
    id = models.BigAutoField(primary_key=True)
    raw_transcript = models.TextField()
    meeting = models.OneToOneField(Meeting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'transcript'


class User(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    full_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10)
    time_zone = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=255)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(db_column='linkedIn', max_length=200, blank=True, null=True)  # Field name made lowercase.
    twitter = models.CharField(max_length=200, blank=True, null=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    profile_pic = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100)
    department = models.ForeignKey(Department, models.DO_NOTHING)
    job_title = models.ForeignKey(OrganizationadminJobtitle, models.DO_NOTHING)
    organization = models.ForeignKey(Organization, models.DO_NOTHING)
    user_audio = models.CharField(max_length=100)
    subscriber_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class UserauthenticationAccesskey(models.Model):
    id = models.BigAutoField(primary_key=True)
    access_key = models.CharField(unique=True, max_length=100)
    attempt = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'userAuthentication_accesskey'


class UserauthenticationUsercalender(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=250)
    calender_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, models.DO_NOTHING)
    platform = models.CharField(max_length=25)

    class Meta:
        managed = False
        db_table = 'userAuthentication_usercalender'


class UserauthenticationUserforgotpassword(models.Model):
    id = models.BigAutoField(primary_key=True)
    file = models.CharField(max_length=100)
    user = models.OneToOneField(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'userAuthentication_userforgotpassword'


class UserauthenticationUserotp(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.CharField(unique=True, max_length=255)
    otp = models.IntegerField()
    retry = models.IntegerField()
    expiry_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'userAuthentication_userotp'


class UserBreakPoints(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_break_point_text = models.TextField()
    meeting = models.OneToOneField(Meeting, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_break_points'
