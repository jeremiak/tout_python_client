### Tout Pythnon API Client

Cient for the Tout API. Check out docs and get keys at [developer.tout.com](http://developer.tout.com)

## Usage

Primary interface is through ToutClient object. Instantiate with an access_token such as:

`t = ToutClient(access_token=TOKEN)`

You can then retrieve the authenticated user (me), an arbitrary user, an arbitrary Tout, or a stream

Each user object has methods that correspond to the API documentation. For example, you can retrieve of all of
user @jeremiak's Touts by using the following:
`   jeremiak = t.get_user(uid='jeremiak')
    jeremiak.get_touts()
    jeremiak.touts #paginated container of user's Touts`

Any paginated container provides an easy interface to walk the paginated result. If we wanted to step through the
Touts that were returned in the above step we can simply do

`jeremiak.touts.next_page()` or `jeremiak.touts.prev_page()`

If we want to see the current page results we access the collection attribute such as 

`jeremiak.touts.collection`

# Examples

`me = t.get_me()`

`gardner = t.get_user(uid='gardner')`

`tout = t.get_tout(uid='7SuIRvWfU3K')`

`stream = t.get_stream(uid='c6i24c')`
