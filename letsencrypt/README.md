# Renewal steps
docker run -it --rm \
-v /home/dougie/htpc-letsencrypt/conf:/etc/letsencrypt \
-v /home/dougie/htpc-letsencrypt/lib:/var/lib/letsencrypt \
-v /home/dougie/htpc-letsencrypt/log:/var/log/letsencrypt \
-v /home/dougie/htpc/letsencrypt/html:/var/www \
certbot/certbot \
certonly --webroot -w /var/www \
--email dmorand@gmail.com --agree-tos --no-eff-email \
-d dougie-fresh.xyz -d dougie-fresh.us

# Old Renewal steps
_as of 2022-04-20_

1. Stop htpc containers
```bash
docker-compose down
```
2.  Start nginx container from this folder
```bash
docker-compose up -d
```
3.  Run `letsencrypt-renew`
4.  Stop nginx container: `docker-compose down`
5.  Restart htpc containers