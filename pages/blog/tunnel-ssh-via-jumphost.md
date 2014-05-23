title: 'Tunnel SSH via jumphost'
published: 2012-03-17
tags: [ linux, ssh, tunnel ]

Nowadays many companies use a so-called _jumphost_s for access to their
servers. While this makes it easier for the network admins and (if configured
properly) more secure, it adds an additional hop for all the users interested
in using the servers behind the jumphost.

So if a programmer wants to reach his dev server the following will happen:

    :::console
    programmer@workstation:~$ ssh jumphost
    programmer@jumphost:~$ ssh devserver
    programmer@devserver:~$ [...]

Combined with some command line switches to ssh that might be necessary to
connect this is a quite tiresome exercise. In order to make life easier for
the programmer the following can be added to the .ssh/config on workstation:

    Host devserver
        ProxyCommand ssh jumphost nc -w5 %h %p

If you (like me) want to use your local ssh agent and the jumphost (actually
`jmp.yourcompany.com`) has ssh running on the non-standard port 12345
(security by obscurity) a complete example could look like this:

    Host jumphost
        ForwardAgent yes
        HostName jmp.yourcompany.com
        Port 12345
    Host devserver
        ProxyCommand ssh jumphost nc -w5 %h %p

Your routine to connect to the devserver would go from

    :::console
    programmer@workstation:~$ ssh -A -p 12345 jmp.yourcompany.com
    programmer@jumphost:~$ ssh devserver
    programmer@devserver:~$ [...]

to

    :::console
    programmer@workstation:~$ ssh devserver
    programmer@devserver:~$ [...]
