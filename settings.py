# ALLOWED_HOSTS=['194.59.165.239',] atau ALLOWED_HOSTS=['*',]



# [Unit]
# Description=gunicorn service
# After=network.target
   
# [Service]
# User=chris
# Group=www-data
# WorkingDirectory=/var/www/gh/goldenhour/
# ExecStart=/var/www/gh/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/gh/goldenhour/awesome.sock AWESOME.wsgi:application
   
# [Install]
# WantedBy=multi-user.target