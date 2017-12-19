# BeerTrendsBC

## Overview

A web application to visualize BC beer and brewery trends.

## Final implementation notes

### What's working

All the features visible on the site are working (e.g. there are no stub pages
or links).

#### Webhooks

Webhooks for updating the database and for providing brewery alerts
are implemented and working but are not registered with BreweryDb, because the
site is not deployed to a stable public server.

You can view the webooks code in `beerdata/views.py` (the functions
`handle_update_beer` and `handle_update_brewery`).

#### Ratings scripts

There are two scripts used to import ratings data into the database. The first
is `scrape/scrape.py`, which performs the actual scraping. Resultant data is in
`scrape/BAratings.json`.

The second is a custom Django management script located in
`trends/management/commands/importratings.py`, which interactively imports
ratings data from a JSON file into the database. It can be run with the command
`python manage.py importratings <input_file>`.

### Access

After running `vagrant up`, visit http://localhost:8001. There is a fair amount
of beer, brewery, and ratings data pre-loaded into the system, as well as a
couple faked brewery notifications.

We've also implemented user registration and password resets, so you can create
your own user and test that if you like. To reset your password, click the
"Lost password?" link on the login page and enter your email. Running from
`localhost`, you'll need to insert `:8001` to the link in the email to get the
link to work. 

To log in, use `quasimodo/beers123`


### Known Bugs
* When navigating back from the recommendation results page, making a new
  recommendation search occasionally causes an exception. This is due to the
geolocation data not being present in the POST data, but because the user
navigated back, the postal code form was not displayed.