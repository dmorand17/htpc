# HTPC Setup using Docker Containers

Currently integrates the following applications:

* [plex](https://www.plex.tv/)
* [sabnzbd](https://sabnzbd.org/)
* [sonarr](https://sonarr.tv/)
* [radarr](https://radarr.video/)
* [portainer](https://www.portainer.io/)
* [watchtower](https://github.com/containrrr/watchtower)

Reverse Proxy: [nginx](https://www.nginx.com/)

## Upgrading
Run `htpc-upgrade` to pull down new docker images, and restart containers

## Security
* Check security of site [here](https://www.ssllabs.com/ssltest/analyze.html?d=dougie-fresh.xyz)
* SSL config can be referenced [here](https://ssl-config.mozilla.org/)
