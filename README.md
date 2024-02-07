# CF_DNS_Updater
Small homebrewed python script to update Cloudflares DNS records with your local IP address. I am in no way affiliated to Cloudflare and all that has been implemented is publically available [here](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records)

## 1. Configure the script
Update the script with the following information:
1. Add your API token obtained from cloudflare by setting the API_TOKEN constant
2. Add you e-mail address (the same used to log in to the cloudflare dashboard), setting the CF_EMAIL constant
3. Add your zone, this can be obtained on the main cloudflare dashboard, setting the ZONE_ID constant
4. Set the domain you wish to update (e.g. subdomain.your_domain.com)

## 2. Dependencies/Requirements
There are no dependencies, requests is used to invoke the http requests.
