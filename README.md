### Tout Pythnon API Client

Cient for the Tout API. Check out docs and get keys at [developer.tout.com](http://developer.tout.com)

## Usage

Primary interface is through ToutClient object. Instantiate with an access_token such as:

`t = ToutClient(access_token=TOKEN)`

You can then retrieve the authenticated user (me), an arbitrary user, an arbitrary Tout, or a stream

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
>>>jeremiak.touts.collection
>>>[Tout nyz307, Tout c3pc8s, Tout rzeae5, Tout on9fgv, Tout dugzfe, Tout 9sf5lc, Tout opeb9x, Tout ge69n2, Tout 0vwqc0, Tout n4oe92, Tout exq9tx, Tout 9tqlti, Tout 22fkl3, Tout ymeiiw, Tout xxicyu, Tout mtsq86, Tout ynviw6, Tout tufmqw, Tout 6a8l5n, Tout q18hft, Tout ffap53, Tout 0ih0xz, Tout 08mk85, Tout 96v00t, Tout k0ztl1, Tout xqg3rb, Tout 78ges8, Tout mw9x3g, Tout zwk75s, Tout vxtvsi, Tout xjonyr, Tout 6rkzei, Tout ltm4aw, Tout menx0j, Tout cd2wm8, Tout y5ngvu, Tout b2iw12, Tout p19ypy, Tout w69wnn, Tout oqpa2x, Tout s3cxoy, Tout rb30bl, Tout i5i5st, Tout q11rgi, Tout ooo1su, Tout kzn6to, Tout ujkup8, Tout 38j8kj, Tout 4h7ldj, Tout 2c9ygi]
```

# Examples

`me = t.get_me()`

`gardner = t.get_user(uid='gardner')`

`tout = t.get_tout(uid='7SuIRvWfU3K')`

`stream = t.get_stream(uid='c6i24c')`
