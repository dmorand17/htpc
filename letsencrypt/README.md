# Renewal steps
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