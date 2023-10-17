from django.core import management


class my_backend_job():
    management.call_command('dbbackup --clean')
