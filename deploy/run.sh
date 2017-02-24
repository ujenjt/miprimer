docker run -d --name nginx -v /root/nginx.conf:/etc/nginx/nginx.conf:ro -p 80:9000  nginx
docker run -d --name miprimer -p 172.17.0.1:4242:4242 ujenjt/miprimer
