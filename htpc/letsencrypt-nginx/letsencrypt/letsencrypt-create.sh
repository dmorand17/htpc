docker run -it --rm -v /home/dougie/mywd1/docker-volumes/letsencrypt/etc/letsencrypt:/etc/letsencrypt \
-v /home/dougie/mywd1/docker-volumes/letsencrypt/var/lib/letsencrypt:/var/lib/letsencrypt \
-v /home/dougie/docker/letsencrypt-nginx/letsencrypt/letsencrypt-site:/data/letsencrypt \
-v "/home/dougie/mywd1/docker-volumes/letsencrypt/var/log/letsencrypt:/var/log/letsencrypt" \
certbot/certbot \
certonly --webroot \
--email dmorand@gmail.com --agree-tos --no-eff-email \
--webroot-path=/data/letsencrypt \
-d dougie-fresh.xyz