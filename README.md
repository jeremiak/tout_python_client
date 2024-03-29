# Tout Python API Client

Cient for the Tout API. Check out docs and get keys at [developer.tout.com](http://developer.tout.com)

## Installation

`python setup.py install`

or `pip install tout`

## Usage

Primary interface is through ToutClient object. Instantiate with an access_token such as:

```
import tout
t = tout.ToutClient(access_token=TOKEN)
```

You can then retrieve the authenticated user (me), an arbitrary user, an arbitrary Tout, or a stream

* [User](https://github.com/jeremiak/tout_python_client#usage)
* [Me](https://github.com/jeremiak/tout_python_client#me)
* [Tout](https://github.com/jeremiak/tout_python_client#tout)

### User

Each user object has methods that correspond to the API documentation. For example, you can retrieve of all of
user @jeremiak's Touts by using the following:
```
jeremiak = t.get_user(uid='jeremiak')
jeremiak.get_touts()
jeremiak.touts #paginated container of user's Touts
```

Any paginated container provides an easy interface to walk the paginated result. If we wanted to step through the
Touts that were returned in the above step we can simply do

`jeremiak.touts.next_page()` or `jeremiak.touts.prev_page()`

If we want to see the current page results we access the collection attribute such as 

```
jeremiak.touts.collection

[Tout b2iw12, Tout p19ypy, Tout w69wnn, Tout oqpa2x, Tout s3cxoy, Tout rb30bl, Tout i5i5st, Tout q11rgi, Tout ooo1su, Tout kzn6to, Tout ujkup8, Tout 38j8kj, Tout 4h7ldj, Tout 2c9ygi]
```

### Me

Me is the authenticated user object, and extends the ToutUser class. It pretty much allows for the same functionality, but also allows for updating of the user information as well as posting of Touts.
Posting Touts requires a proper multipart/form request, which is something we abstract away for you. Just pass the me.post_tout a Python file object as `tout_file` and you're good to go.

```
me = t.get_me()
tout_to_post = open('tout.mp4')
me.post_tout(tout_file=tout_to_post)
```


### Tout

Each Tout object allows for the text to be set on that Tout, for the changes to be saved if the current user owns the Tout, and to delete the Tout (again if the current user is the owner).
Every object has a reference to the access_token that was used to retrieve it. This allows you to update or delete a Tout easily.

```
tout_to_update = jeremiak.tout.collection[0]
tout_to_update.update_tout(text='New text goes here') # changes tout._changed to True
tout_to_update.save() # will return an error if the token that was used to retrieve the Tout doesn't give proper ownership

tout_to_delete = jeremiak.touts.collection[1]
tout_to_delete.delete(confirm=True) # no going back, so make sure to pass in the confirm parameter otherwise the transaction won't happen
```

## Examples

`me = t.get_me()`

`gardner = t.get_user(uid='gardner')`

`tout = t.get_tout(uid='7SuIRvWfU3K')`

`stream = t.get_stream(uid='c6i24c')`
