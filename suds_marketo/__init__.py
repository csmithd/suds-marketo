from suds.client import Client as SudsClient
import version
import auth

__author__ = version.AUTHOR
__version__ = version.VERSION

class Client:
    def __init__(self, soap_endpoint=None, user_id=None, encryption_key=None):
        if not soap_endpoint or not isinstance(soap_endpoint, str):
            raise ValueError('Must supply a soap_endpoint as a non empty string.')

        if not user_id or not isinstance(user_id, (str, unicode)):
            raise ValueError('Must supply a user_id as a non empty string.')

        if not encryption_key or not isinstance(encryption_key, str):
            raise ValueError('Must supply a encryption_key as a non empty string.')

        self.soap_endpoint = soap_endpoint
        self.user_id = user_id
        self.encryption_key = encryption_key

        self.client = SudsClient('http://app.marketo.com/soap/mktows/2_0?WSDL')
        # Make easy the access to the types
        self.valid_types = []
        for valid_type in self.client.sd[0].types:
            self.valid_types.append(valid_type[0].name)

    def __getattribute__(self, name):
        if name != 'valid_types' and name in self.valid_types:
            # if the attribute is one of the Types
            return self.client.factory.create(name)
        else:
            return super(Client, self).__getattribute__(name)

    def set_header(self):
        wsse = auth.header(self.user_id, self.encryption_key)
        self.client.set_options(wsse=wsse)

