# Rather than using the docker-compose.yml file a container can be spun up as follows
#
docker run -ti --rm --name nginx-letsencrypt \
-v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf \
-v $(pwd)/letsencrypt-site:/usr/share/nginx/html \
-p 80:80 \
-d \
nginx:alpine

# Run letsencrypt in test mode
docker run -it --rm -v /home/dougie/docker-volumes/etc/letsencrypt:/etc/letsencrypt \
-v /home/dougie/docker-volumes/var/lib/letsencrypt:/var/lib/letsencrypt \
-v /home/dougie/docker-app-conf/letsencrypt-nginx/src/letsencrypt/letsencrypt-site:/data/letsencrypt \
-v "/home/dougie/docker-volumes/var/log/letsencrypt:/var/log/letsencrypt" certbot/certbot certonly --webroot \
--register-unsafely-without-email --agree-tos --webroot-path=/data/letsencrypt --staging -d dougie-fresh.xyz

# Run letsencrypt to get prod cert
docker run -it --rm -v /home/dougie/docker-volumes/etc/letsencrypt:/etc/letsencrypt \
-v /home/dougie/docker-volumes/var/lib/letsencrypt:/var/lib/letsencrypt \
-v /home/dougie/docker-app-conf/letsencrypt-docker-nginx/src/letsencrypt/letsencrypt-site:/data/letsencrypt \
-v "/home/dougie/docker-volumes/var/log/letsencrypt:/var/log/letsencrypt" \
certbot/certbot \
certonly --webroot \
--email dmorand@gmail.com --agree-tos --no-eff-email \
--webroot-path=/data/letsencrypt -d dougie-fresh.xyz