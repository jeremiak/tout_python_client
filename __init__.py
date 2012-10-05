import httplib, mimetypes, types, requests
from tout_user import ToutUser
from tout_me import ToutMe
from tout_tout import Tout

class ToutAPIClient(object):
    def __init__(self, access_token=None):
        self.protocol = 'https'
        self.base_url = 'api.tout.com'
        if access_token is not None:
            self.access_token = access_token
        else:
            print "API is worthless without an access_token. Set yours on the ToutAPIClient object with ToutAPIClient.access_token = XX"

    def post_tout(self, tout_file=None):
        if self.access_token is None:
            return "Need a token"
        else:
            if type(tout_file) is types.FileType:
                content_type, body = self.encode_multipart_formdata([('access_token', self.access_token)], [('tout[data]', tout_file.name(), tout_file.read())])
                tout_file.close()

                h = httplib.HTTPSConnection(self.base_url)
                headers = {
                    'User-Agent': 'tout-python-client',
                    'Content-Type': content_type
                    }
                h.request('POST', '/api/v1/touts.json', body, headers)
                res = h.getresponse()

            else:
                return "Please pass in a Tout video file"

    def encode_multipart_formdata(self, fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------bound@ry_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % self.get_content_type(filename))
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def get_content_type(self, filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

