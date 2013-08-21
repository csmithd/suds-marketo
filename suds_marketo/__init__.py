from suds.client import Client as SudsClient
import version
import auth

__author__ = version.AUTHOR
__version__ = version.VERSION

class Client(object):
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

        self.suds_client = SudsClient('http://app.marketo.com/soap/mktows/2_0?WSDL',
                location=soap_endpoint)
        # Make easy the access to the types and methods
        self.suds_types = []
        self.suds_methods = []
        for suds_type in self.suds_client.sd[0].types:
            self.suds_types.append(suds_type[0].name)
        for suds_method in self.suds_client.sd[0].service.ports[0].binding.operations:
            self.suds_methods.append(suds_method)

    def __getattribute__(self, name):
        if name not in ('suds_types', 'suds_methods') and name in self.suds_types:
            # if the attribute is one of the Types
            return self.suds_client.factory.create(name)
        elif name not in ('suds_types', 'suds_methods') and name in self.suds_methods:
            return self.suds_client.service.__getattr__(name)
        else:
            return super(Client, self).__getattribute__(name)

    def set_header(self):
        soapheaders = auth.header(self.user_id, self.encryption_key)
        self.suds_client.set_options(soapheaders=soapheaders)


    def call_service(self, name, *args, **kwargs):
        self.set_header()
        self.__getattribute__(name)(*args, **kwargs)

    def get_lead(self, email):
        lead_key = self.LeadKey
        lead_key.keyType = self.LeadKeyRef.EMAIL
        lead_key.keyValue = email
        self.call_service('getLead', lead_key)


