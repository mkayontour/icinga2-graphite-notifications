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
