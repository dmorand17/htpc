# Rather than using the docker-compose.yml file a container can be spun up as follows
#
docker run -it --rm --name nginx-letsencrypt \
-v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf \
-v $(pwd)/letsencrypt-site:/usr/share/nginx/html \
-p 80:80 \
-d \
nginx:alpine

# Run letsencrypt in test mode
docker run -it --rm \
-v acme-challenge:/var/www/challenge/.well-known/acme-challenge \
-v /home/dougie/docker-volumes/etc/letsencrypt:/etc/letsencrypt \
-v /home/dougie/docker-volumes/var/lib/letsencrypt:/var/lib/letsencrypt \
-v /home/dougie/docker/letsencrypt-docker-nginx/src/letsencrypt/letsencrypt-site:/var/www \
-v "/home/dougie/docker-volumes/var/log/letsencrypt:/var/log/letsencrypt" \
certbot/certbot \
certonly --webroot -w /var/www/challenge \
--register-unsafely-without-email --agree-tos \
--staging \
-d dougie-fresh.xyz

# Run letsencrypt to get prod cert
docker run -it --rm \
-v acme-challenge:/var/www/challenge/.well-known/acme-challenge \
-v /home/dougie/docker-volumes/letsencrypt/etc/letsencrypt:/etc/letsencrypt \
-v /home/dougie/docker-volumes/letsencrypt/var/lib/letsencrypt:/var/lib/letsencrypt \
-v /home/dougie/docker/letsencrypt-docker-nginx/src/letsencrypt/letsencrypt-site:/var/www \
-v "/home/dougie/docker-volumes/letsencrypt/var/log/letsencrypt:/var/log/letsencrypt" \
certbot/certbot \
certonly --webroot -w /var/www/challenge \
--email dmorand@gmail.com --agree-tos --no-eff-email \
-d dougie-fresh.xyz

# Renew certificates
docker run -t --rm \
-v acme-challenge:/var/www/challenge/.well-known/acme-challenge \
-v /home/dougie/docker-volumes/letsencrypt/etc/letsencrypt:/etc/letsencrypt \
-v /home/dougie/docker-volumes/letsencrypt/var/lib/letsencrypt:/var/lib/letsencrypt \
-v /home/dougie/docker/letsencrypt-docker-nginx/src/letsencrypt/letsencrypt-site:/var/www \
-v "/home/dougie/docker-volumes/letsencrypt/var/log/letsencrypt:/var/log/letsencrypt" \
certbot/certbot \
renew --dry-run \
-d dougie-fresh.xyz