import requests
import json
from pathlib import Path

with open('status_code_data.json', 'r') as f:
    data = json.load(f)

Path("output/").mkdir(parents=True, exist_ok=True)

for i in data['errors']:
	with open('template.html') as f:
		content = f.read()
		new_content = content
		error_code = int(i['code'])

		new_content = new_content.replace('$ERROR_CODE', i['code'])
		new_content = new_content.replace('$ERROR_NAME', i['name'])
		with open('output/'+i['code']+'.html', 'w') as output_file:
			output_file.write(new_content)

with open('nginx_error_pages.conf', 'w') as f:
	for i in data['errors']:
		v = int(i['code'])
		print("error_page %d /nginx-error-pages/%d.html;" % (v,v), file=f)

	print("""
location ~ /(4[01235][0-9]|5[01][0-9])\.html {
	root /srv/http/nginx-error-pages/output/;
	sub_filter '%{HOSTNAME}' $host;
	sub_filter_once off;
	allow all;
	internal;
}""", file=f)
