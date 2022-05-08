<img style="float:left;" src="https://www.gstatic.com/images/branding/product/1x/google_domains_64dp.png">

# Google Domains DDNS Updater - Docker

Use this docker container to update your Google Domains Dynamic DNS service.

I wanted to write a custom update script for updating my Google Domains DDNS records that I could easily run on my NAS. I had previously been using another script (`dragoncube/google-domains-ddns`) but I found it a bit tedious to have to manually edit volumes to configure the options. I think it is far more convenient to use environmental variables for this purpose (particularly when using a service such as Portainer).

### How to use:
Run the image with environmental variables set correctly  
e.g.
```bash
docker run -d --name gdomains_ddns -e USERNAME=**redacted** -e PASSWORD=**redacted** -e HOSTNAME=limeparallelogram.uk limeparallelogram/googledomains_ddns
```
Be sure to check the logs to ensure everything works correctly
```bash
docker logs gdomains_ddns
```

### Required Environment Variables:  
```yaml
USERNAME="UNSET" # google domains username*
PASSWORD="UNSET" # google domains password*
HOSTNAME="UNSET" # the host you are updating
```
\* These are **not** your google account details.

### Optional Environment Variables:
```yaml
TIMEOUT=8 # The time in mins to wait between updates (default=8)
```

### Example docker-compose
For easy backup, you may chose to create a compose file for all of of your DDNS domains. For example, this could look like:
```yaml
version: '3'
services:
    ddns1:
        image: limeparallelogram/googledomains_ddns
        restart: always
        environment:
         - USERNAME=**redacted**
         - PASSWORD=**redacted**
         - HOSTNAME=limeparallelogram.uk
    ddns2:
        image: limeparallelogram/googledomains_ddns
        restart: always
        environment:
         - USERNAME=**redacted**
         - PASSWORD=**redacted**
         - HOSTNAME=admin.limeparallelogram.uk
```


### Docker Hub:
https://hub.docker.com/r/limeparallelogram/googledomains_ddns

### Thank you
I hope this script works for you and serves your needs. If you have any issues or suggestions, feel free to use the GitHub issues to flag them up. 

