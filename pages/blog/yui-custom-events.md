title: 'YUI custom events'
published: 2012-03-22
tags: [ yui, events, javascript, accordion ]

When finally being able to
[hook into the lifecycle of the gallery-node-accordion](/blog/yui-inheritance/)
module, I wanted to use events that other parts of the code could subscribe
to. That way I wouldn't need to hard-wire otherwise unrelated business logic.

My first approach was to fire custom events on the corresponding nodes of the accordion:
  * accordion root fires `accordion:ready`
  * accordion section fires `accordion:item:open` and `accordion:item:close`

That way I would be able to subscribe to those events via Y, the accordion
root or the corresponding section. In order to benefit from event bubbling and
be able to subscribe in other parts of the code (with the same Y object) I
needed to publish the events for the corresponding nodes:

    :::js
    accordion.publish('accordion:ready', { fireOnce: true, emitFacade: true, broadcast: 1 });
    accordion.all('.yui3-accordion-item').each(function(node) {
        node.publish('accordion:item:open', { emitFacade: true, broadcast: 1 });
        node.publish('accordion:item:close', { emitFacade: true, broadcast: 1 });
    });

While I liked the concept and flexibility of firing those events on certain
nodes it turned out that there are certain limitations to that approach.

    :::js
    YUI().use('node', function(Y) {
        Y.use('gallery-node-accordion', function() {
            accordion.fire('accordion:ready');
        });
        Y.use('node', function() {
            Y.on('accordion:ready', function(e) { ... }, '.yui3-accordion-item');
        });
        Y.use('io', function() {
            Y.on('accordion:ready', function(e) { ... }, '.yui3-accordion-item');
        });
    });

In the above code the subscriber in `Y.use('node')` triggers, but the
subscriber in `Y.use('io')` does not. While in theory both should trigger
(broadcasting being enabled and both sharing the same Y instance), there seem
to be certain limitations to broadcasting events fired from a node. These
restrictions seem to be specific to certain modules and/or if they were
already loaded when the event is fired, but I don't fully understand the
design decision behind it.

The easy solution is to fire and subscribe to custom events on the Y instance
rather than using the specific nodes. You will loose the ability to limit your
event subscription to a specific accordion instance or item via generic
accordion:* events, but using application specific events will make your code
cleaner and easier to understand. So I introduced the events
`people:accordion:ready`, `people:section:open` and `people:section:close`
leading to the following code:

    :::js
    Y.use('gallery-node-accordion', function() {
        Y.publish('people:accordion:ready', { fireOnce: true });
        Y.publish('people:section:open');
        Y.publish('people:section:close');
        Y.fire('people:accordion:ready');
    });
    Y.use('node', function() {
        Y.on('people:accordion:ready', function(e) { ... });
    });
    Y.use('io', function() {
        Y.on('people:section:open', function(e) { ... });
        Y.on('people:section:close', function(e) { ... });
    });
