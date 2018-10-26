# Notifications with Graphite

## Installation

Clone or download the full repository into `/etc/icinga2/scripts` and copy the graphite-notifications.conf into your Icinga 2 configuration folder. 


## Requirements

Those python modules are needed on the system:
* jinja2
* bs4
* requests
* base64

## Templating

The HTML Templates can be copied and modified. Add your own template and reference it in the script.
Templates are provided via the jinja2 templating engine. Please have a look at the documentation for reference.
