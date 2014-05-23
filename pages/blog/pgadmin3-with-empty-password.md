title: 'PGadmin3 with empty password'
published: 2013-08-22
tags: [ postgresql, password ]

After an update of [PGadmin3](http://www.pgadmin.org/) I was no longer able to
save empty passwords for servers. Therefore whenever I wanted to connect to a
server I had to click OK on the password dialog.

As this became annoying I found out that the only difference between my old
servers (without the need for a password dialog) and my new servers was in the
`.pgpass` file in my home directory.

This file contains one saved password per line and follows the syntax:

    hostname:port:database:username:password

So I quickly added two new lines for my newly added servers using `*` for
database and leaving password empty and got rid of the password dialog.
