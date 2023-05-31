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

After that, let's change `/etc/mysql/my.cnf` file, change

.. code-block:: shell

     bind-address = 127.0.0.1

to

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

    sudo ufw allow from <remote_IP_address> to any port 3306

.. _`Setup and run nginx server with api`:
Setup and run nginx server with api
-----------------------------------




