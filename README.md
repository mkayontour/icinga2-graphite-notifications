# Notifications with Graphite

## Installation

Clone or download the full repository into `/etc/icinga2/scripts` and copy the `check_command.conf` into your Icinga 2 configuration folder and reload Icinga 2.


## Requirements

Those python modules are needed on the system:
* pip install Jinja2
* pip install bs4
* pip install requests
* pip install smtplib
* pip install argparse

## Templating

The HTML Templates can be copied and modified. Add your own template and reference it in the script.
Templates are provided via the jinja2 templating engine. Please have a look at the documentation for reference.

### Choose Templates

The Templating engine allows to customize or add own templates.
Just use the custom variable:
```
vars.graphite_notification_template = "customer-x.html.j2"
```
Modify the content to your needs or your customer needs and add it to a template which is specific for the customer or user.

### Add your own logo

Put your logo into the `/img/` folder and modify the variable  
