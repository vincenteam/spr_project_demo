starting the website:
<br>$ source venv/bin/activate
<br>$ python app/manage.py runserver


Then the website should be accessible at the address given by the last command, the search service is accessible via <given addresse>/search
In order to test it POST request need to be sent:
exemple of POST request to start a search:

<br>

>POST /search/ HTTP/1.1
>Host: localhost:8000
>Cookie: sessionid=c0epsjiwa46ywutp48z2v7uae5hdivd3
>Content-Length: 314
>Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

>----WebKitFormBoundary7MA4YWxkTrZu0gW
>Content-Disposition: form-data; name="new_search"

>1
>----WebKitFormBoundary7MA4YWxkTrZu0gW
>Content-Disposition: form-data; name="lat"

>37.190706
>----WebKitFormBoundary7MA4YWxkTrZu0gW
>Content-Disposition: form-data; name="lon"

>-42.541450
>----WebKitFormBoundary7MA4YWxkTrZu0gW
