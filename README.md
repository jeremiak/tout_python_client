### Tout Pythnon API Client

Cient for the Tout API. Check out docs and get keys at [developer.tout.com](http://developer.tout.com)

## Usage

Primary interface is through ToutClient object. Instantiate with an access_token such as:

`t = ToutClient(access_token=TOKEN)`

You can then retrieve the authenticated user (me), an arbitrary user, an arbitrary Tout, or a stream

# Examples

`me = t.get_me()`

`gardner = t.get_user(uid='gardner')`

`tout = t.get_tout(uid='7SuIRvWfU3K')`

`stream = t.get_stream(uid='c6i24c')`
