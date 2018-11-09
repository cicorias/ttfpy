# Nginx configuration...
Nginx is used to serve the static HTML file - as an index.html file. Images are then served from the `/images` path on the host using the following example configurations.



## Installation Ubuntu

```bash
sudo apt update
sudo apt install nginx -y
```

### Starting, Stopping, Restart and Reload
Nginx is by default under systemctl on Ubuntu. It can also be managed via 

#### Starting Nginx if stopped for some reason
```
sudo /etc/init.d/nginx start
```

#### Get the status of the daemon
```
sudo /etc/init.d/nginx status
```

#### Stopping Nginx
```
sudo /etc/init.d/nginx stop
```
#### Full restart of Nginx daemon
```
sudo /etc/init.d/nginx restart
```
#### Reload the Content without a restart
Preferred for quick changes to the site content.
```
sudo /etc/init.d/nginx reload
```

## Assumptions
This configuration assumes:
* the TTF images are located in a path on the host machine.  This is then mapped on nginx to the `/images` path.
* An index.html file is present on a location on the host machine, which the root and absolute path to that `index.html` file is mapped via the `alias` in the `nginx.conf` settings.


## Configuration Changes
The following example assumes that the TTF `index.html` file is located in the file system at `/c/g/irc/py/ttf-html` -- and the images are located as a sub path of that directory.  Ensure that the right hand side of the setting matches the host configuration.

The default site is managed in nginx in the file `/etc/nginx/sites-enabled/default`.

Edit this file via:
```
sudo vi /etc/nginx/sites-enabled/default

```



```
location /images {
        alias /c/g/irc/py/ttf-html/images/;

}
location /reports {
        alias /c/g/irc/py/ttf-html/;
}
```

> NOTE: after making these changes - you can reload nginx via `sudo /etc/init.d/nginx reload`.


### Full example configuration

This is a full `/etc/nginx/sites-enabled/default` example configuration that listens on port `8000`.

```
server {
        listen 8000 default_server;
        listen [::]:8000 default_server;

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                try_files $uri $uri/ =404;
        }
        location /images {
                alias /c/g/irc/py/ttf-html/images/;
        }
        location /reports {
                alias /c/g/irc/py/ttf-html/;
        }
}