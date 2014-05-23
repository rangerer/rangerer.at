title: 'YUI inheritance'
published: 2012-03-22
tags: [ yui, inheritance, javascript, accordion ]

At work we are using the
[gallery-node-accordion](http://yuilibrary.com/gallery/show/node-accordion)
module from the YUI gallery to group content into sections. While the module
is quite useful to transform already existing content into an accordion
structure, it falls short on ways to hook into the accordion lifecycle. A
typical task might be to load ads when opening a section or scroll to the head
of the section once the accordion animation is complete. Normally you could
accomplish those hooks by firing events for those specific moments in the
accordion lifecycle and let users subscribe to those events to add business
logic. Unfortunately caridy (the developer of gallery-node-accordion) did only
leave todo comments instead of actually firing those events.

The proper solution would have been to fork caridys work from github, add
those events, post a pull request for caridy and point our application to use
my version of `gallery-node-accordion`. I decided to take the easy option and
create a class that would inherit from `Y.Plugin.NodeAccordion` and overwrite
the methods that I want to fire events for.

    :::js
    Y.namespace('Plugin').PeopleAccordion = Y.Base.create('PeopleAccordion', Y.Plugin.NodeAccordion, [], {
        initializer: function(config) { ... },
        _openItem: function(item) { ... }
    }, { NS: 'accordion' });

It took me quite a while to get the above code working and have a functioning
`Y.Plugin.PeopleAccordion` class that I could use. The main reason was that
although `NodeAccordion` does already supply the static NS attribute it needs
to be supplied by `PeopleAccordion` as well.

When using `Y.Base.create` the initializer function is augmented with the one
from `NodeAccordion` and therefore you can simply add your code and both
functions will be called. So the only thing left to do was firing an event in
`_openItem` and forward the call to `NodeAccordion._openItem`. After playing
around for another few hours I came to the conclusion that there is no way to
call the parents `_openItem` method from the `PeopleAccordion` instance. I was
able to get a prototype of `NodeAccordion` and call (or apply) the `_openItem`
method, but as that method needs to operate on the instances attributes it was
no good.

I was at a dead end and had to resort to replacing the click event handlers in
`PeopleAccordion` with my own.

    :::js
    node.plug(Y.Plugin.Accordion, { ... });
    node.accordion._eventHandler.detach();
    node.accordion._eventHandler = this.delegate('click', function(e) {
        // custom code
        node.accordion.toggleItem( e.target );
        e.target.blur();
        e.halt();
    }, '.yui3-accordion-item-trigger');
