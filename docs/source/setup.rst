Setup
======

For setup you need 3 things:

1. `Setup mysql server`_
2. `Setup and run nginx server with api`_
3. Set up and run Bot.py script

.. _`Setup mysql server`:
Setup mysql server
------------------

First of all, let's download mysql community server:

.. code-block:: shell

    $ sudo apt update
    $ sudo apt install mysql-server
    $ sudo systemctl start mysql.service


Next, we need, to secure mysql:

.. code-block:: shell

    $ sudo mysql_secure_installation

After that, let's change `/etc/mysql/my.cnf` file. Instead of:

.. code-block:: shell

     bind-address = 127.0.0.1

Write that:

.. code-block:: shell

     bind-address = 0.0.0.0

Now:

.. code-block:: shell

    $ sudo systemctl restart mysql

Then, we need to crete remote user:

.. code-block:: shell

    sudo mysql
    mysql> RENAME USER 'sammy'@'localhost' TO 'sammy'@'remote_server_ip';
    mysql> GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'sammy'@'remote_server_ip' WITH GRANT OPTION;
    mysql> FLUSH PRIVILEGES;
    mysql> exit

If you using ufw, you need to grant access:

.. code-block:: shell

    $ sudo ufw allow from <remote_IP_address> to any port 3306

.. _`Setup and run nginx server with api`:
Setup and run nginx server with api
-----------------------------------

Before starting, we need to download requires packages:

.. code-block:: shell

    $ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
    $ sudo apt install python3-venv

Next, you need to clone equipmentIssuance repo, after that:

.. code-block:: shell

    $ python3.11 -m venv myvenv
    $ source myvenv/bin/activate
    (myvenv) $ pip install -r requirements.txt

Also, you need `wheel` and `uwsgi`:

.. code-block:: shell

    (myvenv) $ pip install wheel uwsgi
    (myvenv) deactivate

Now, let's create uWSGI configuration file:

.. code-block:: shell

    $ nano ~/api/api.ini

.. code-block:: shell
    :caption: ~/api/api.ini

    [uwsgi]
    module = wsgi:app

    master = true
    processes = 5

    socket = myproject.sock
    chmod-socket = 660
    vacuum = true

    die-on-term = true


Now, we need systemd unit file:

.. code-block:: shell

    $ sudo nano /etc/systemd/system/api.service

Write:

.. code-block:: shell
    :caption: ~/etc/systemd/system/api.service

    [Unit]
    Description=uWSGI instance to serve Api
    After=network.target

    [Service]
    User=`user`
    Group=www-data
    WorkingDirectory=/home/`user`/api
    Environment="PATH=/home/`user`/api/myvenv/bin"
    ExecStart=/home/`user`/api/myvenv/bin/uwsgi --ini api.ini

    [Install]
    WantedBy=multi-user.target

Now, we need to configure Nginx to Proxy Request, but firstly, we need to create
a SSL certificate:

.. code-block:: shell

    $ sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt

Then:

.. code-block:: shell

    $ sudo openssl dhparam -out /etc/nginx/dhparam.pem 4096


Then:

.. code-block:: shell

    $ sudo nano /etc/nginx/snippets/self-signed.conf

Write:

.. code-block:: shell
    :caption: ~/etc/nginx/snippets/self-signed.conf

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;


Then:

.. code-block:: shell

    sudo nano /etc/nginx/snippets/ssl-params.conf

Write:

.. code-block:: shell
    :caption: ~/etc/nginx/snippets/ssl-params.conf

    ssl_protocols TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_dhparam /etc/nginx/dhparam.pem;
    ssl_ciphers EECDH+AESGCM:EDH+AESGCM;
    ssl_ecdh_curve secp384r1;
    ssl_session_timeout  10m;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off;
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    # Disable strict transport security for now. You can uncomment the following
    # line if you understand the implications.
    #add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

Now we ready for configuring:

.. code-block:: shell

    sudo nano /etc/nginx/sites-available/api

Write:

.. code-block:: shell
    :caption: ~/etc/nginx/sites-available/api

    server {
        listen 443 ssl;
        listen [::]:443 ssl;
        server_name `your_domain` `www.your_domain`;
        listen 443 ssl;
        listen [::]:443 ssl;
        include snippets/self-signed.conf;
        include snippets/ssl-params.conf;

        location / {
            include uwsgi_params;
            uwsgi_pass unix:/home/`user`/api/api.sock;
        }
    }
    server {
        listen 80;
        listen [::]:80;

        server_name `your_domain.com` `www.your_domain.com`;

        return 301 https://$server_name$request_uri;
    }

Now link this file:

.. code-block:: shell

    sudo ln -s /etc/nginx/sites-available/api /etc/nginx/sites-enabled

And:

.. code-block:: shell

    sudo nginx -t
    sudo systemctl restart nginx


