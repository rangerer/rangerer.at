title: 'Mailserver and Nameserver change'
published: 2012-01-03
tags: [ mail, netcup, postfix ]

End of 2012 my provider [netcup](http://www.netcup.de/) decided to change
their nameservers. In an email to all their customers they explained that
`/etc/resolv.conf` should be changed accordingly.

Unfortunately they didn't state that already running daemons (like postfix -
my MTA) would not benefit from that change. So it was only by accident that I
discovered, that outbound mails wouldn't be sent any more. The reason was that
postfix was unable to find the MX records for domains he should be sending
mails to.

It was an easy fix - just restarted postfix (and dovecot, just to be sure) and
I learned some nifty commands while I was at it.

  * `mailq` - lists all mails queued currently
  * `postfix flush` - tries to send all deferred mails now

Note: debian systems have scripts under `/etc/resolvconf` that should be
executed whenever `resolv.conf` changes. In my case it would feed the new
`/etc/resolv.conf` to postfix and do a postfix reload.
