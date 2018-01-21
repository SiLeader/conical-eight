Conical Eight
=======

&copy; 2018 SiLeader.

## Overview
Conical Eight is simple web site development tool and system.

### Features
+ Small application
+ Easy to create or edit pages

## How to use
If you need `favicon.ico` and other files, install to these files in `static` directory.
### Initial setup
1. Install to your server.
1. Edit `templates/layout.html` for your site.
1. Edit `settings.py` for your site.
1. Run `user.py` as script file to add new administrator.
1. Launch application.

### Post new page
1. Access to `(site host)/secrets/login` and login as administrator.
1. Select `New Page` and post your page.

### Edit existing page
1. Access to `(site host)/secrets/login` and login as administrator.
1. Select page id in `Update page`.

### Remove page
1. Access to `(site host)/secrets/login` and login as administrator.
1. Select page id in `Remove page`.

## Routing rule
+ `(site host)/<page-id>`

If `page-id` is `#top`, route to `(site host)/`.

## Dependencies
+ MongoDB

### Python modules
+ pymongo
+ Flask
+ Flask-WTF
+ markdown2

## License
Apache License 2.0 (See LICENSE)
