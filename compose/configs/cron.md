Como usuario `crontab -e`

```bash
MAILTO=snicoper@snicoper.com

0 1 * * * /var/webapps/snicoper.com/cron/haystack_update_index.sh
2 1 * * * /var/webapps/snicoper.com/cron/postgres_db_backup.sh
4 1 * * * /var/webapps/snicoper.com/cron/clear_sessions.sh
6 1 * * * /var/webapps/snicoper.com/cron/ping_google.sh
8 1 * * * /var/webapps/snicoper.com/cron/media_backup.sh
```

Como root `sudo crontab -e`

```bash
MAILTO=snicoper@snicoper.com

30 2 * * 1 /usr/bin/certbot renew >> /var/log/le-renew.log
35 2 * * 1 /usr/bin/systemctl reload nginx
```
