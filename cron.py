import os
import django

def execute_command():
	from appaaa.models import Comment
	try:
		print('Run shell script')
	except Exception as e:
		print(e)

if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HelloDjango.settings")
	django.setup()
	execute_command()