docker build -t cybersecurity_img .
docker container run -p 5000:5000 --name cybersecurity_ctr cybersecurity_img