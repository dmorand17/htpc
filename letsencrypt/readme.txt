# Rather than using the docker-compose.yml file a container can be spun up as follows
#
docker run -it --rm --name nginx-letsencrypt \
-v $(pwd)/nginx.conf:/etc/nginx/conf.d/default.conf \
-v $(pwd)/html:/var/www \
-p 80:80 \
-d \
nginx:alpine

# Run letsencrypt in test mode
docker run -it --rm \
-v /home/dougie/docker-volumes/letsencrypt/conf:/etc/letsencrypt \
-v /home/dougie/docker-volumes/var/lib/letsencrypt:/var/lib/letsencrypt \
-v "/home/dougie/docker-volumes/var/log/letsencrypt:/var/log/letsencrypt" \
-v /home/dougie/htpc/letsencrypt/html:/var/www \
certbot/certbot \
certonly --webroot -w /var/www \
--register-unsafely-without-email --agree-tos \
--staging \
-d dougie-fresh.xyz

# Run letsencrypt to get prod cert
docker run -it --rm \
-v /home/dougie/docker-volumes/letsencrypt/conf:/etc/letsencrypt \
-v /home/dougie/docker-volumes/letsencrypt/var/lib/letsencrypt:/var/lib/letsencrypt \
-v "/home/dougie/docker-volumes/letsencrypt/var/log/letsencrypt:/var/log/letsencrypt" \
-v /home/dougie/htpc/letsencrypt/html:/var/www \
certbot/certbot \
certonly --webroot -w /var/www \
--email dmorand@gmail.com --agree-tos --no-eff-email \
-d dougie-fresh.xyz -d dougie-fresh.us

# Renew certificates
docker run -t --rm \
-v /home/dougie/docker-volumes/letsencrypt/conf:/etc/letsencrypt \
-v /home/dougie/docker-volumes/letsencrypt/var/lib/letsencrypt:/var/lib/letsencrypt \
-v "/home/dougie/docker-volumes/letsencrypt/var/log/letsencrypt:/var/log/letsencrypt" \
-v /home/dougie/htpc/letsencrypt/html:/var/www \
certbot/certbot \
renew --dry-run \
-d dougie-fresh.xyz -d dougie-fresh.us