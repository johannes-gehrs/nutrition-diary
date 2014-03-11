nothing:
	@echo "default target does nothing."

reset:
	./manage.py sqlclear app admin | python manage.py dbshell
	./manage.py syncdb
