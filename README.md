Instruments
===========

Flask based login manager with support for plugin 'blueprints'

Requires PostgreSQL

and:
- psycopg2
- Flask

## Blueprints

I've built 3 usable blueprints so far:

- [Pulse - Simple Web Stats](https://github.com/MalphasWats/pulse)
- [subMarks - Bookmarking](https://github.com/MalphasWats/subMarks)
- [Electrostatic - Static blog generator](https://github.com/MalphasWats/electrostatic)

The best way to install these is to clone the repos somewhere on your system, then symlink the
package directory.

I set my server up as follows:

    ~/
      projects/
        instruments/
          instruments/
            __init__.py
            core.py
            database.py
            static/
              ...
            templates/
              ...
        pulse/
          pulse/
            __init__.py
            core.py
            database.py
            ...
        subMarks/
          subMarks/
            __init__.py
            core.py
            ...
        electrostatic/
          electrostatic/
            ...
      public_html/
        instruments/
          instruments.wsgi
          settings.cfg
          blueprints/
            pulse => ~/projects/pulse/pulse
            subMarks => ~/projects/subMarks/subMarks
            electrostatic => ~/projects/electrostatic/electrostatic
        electrostatic-blog-website/
          ...website files..
          templates/
            ...jinja2 templates...
            

I currently use [Apache2 with `mod_wsgi`](http://www.subdimension.co.uk/2012/04/24/Deploying_Flask_to_Apache.html) to run everything, with instruments on a separate sub-domain to the website generated by electrostatic, but you should be able to run it all from a single domain.

to create the database, open an interactive Python session:

    from instruments.database import create_tables
    
    create_tables("dbname=database_name user=database_username password=database_password", "forename", "surname", "email_address", "user.name", "plaintext_password")
    
You can change the password from the Admin page once you log in. There currently isn't a way to add users other than the initial one specified here! Actual user management needs a fair bit of work still. You can add users to the database manually, passwords are stored as a sha512 hash.

Hopefully that makes enough sense to make it go.