from datetime import datetime
from rfc3339 import rfc3339
from suds.client import Client as SudsClient
import version

__author__ = version.AUTHOR
__version__ = version.VERSION

import hmac
import hashlib

def sign(message, encryption_key):
    digest = hmac.new(encryption_key, message, hashlib.sha1)
    return digest.hexdigest().lower()

class InvalidLeadKeyType(Exception): pass

class Client(object):

    """
    Wrapper of the Marketo SOAP Api

    Marketo SOAP Api doc: https://jira.talendforge.org/secure/attachmentzip/unzip/167201/49761%5B1%5D/Marketo%20Enterprise%20API%202%200.pdf
    """

    MARKETO_WSDL = 'http://app.marketo.com/soap/mktows/2_0?WSDL'
    """Url of the Marketo wsdl file"""

    suds_types = []
    """List of the Marketo SOAP Api types"""
    suds_methods = []
    """List of the Marketo SOAP Api methods"""
    soap_endpoint = None
    """Marketo SOAP endpoint"""
    user_id = None
    """Marketo SOAP user ID"""
    encryption_key = None
    """Marketo SOAP encryption key"""
    suds_client = None
    """Consolidated API for consuming web services"""


    def __init__(self, soap_endpoint, user_id, encryption_key):
        """
        Instantiate the suds client and add the SOAP types and methods to the list of attributes
        How to get the Marketo SOAP parameters: See page 4 of the Marketo SOAP Api doc.
        """
        self.soap_endpoint = soap_endpoint
        self.user_id = user_id
        self.encryption_key = encryption_key

        self.suds_client = SudsClient(Client.MARKETO_WSDL,
                location=soap_endpoint)
        # Make easy the access to the types and methods
        for suds_type in self.suds_client.sd[0].types:
            self.suds_types.append(suds_type[0].name)
        for suds_method in self.suds_client.sd[0].service.ports[0].binding.operations:
            self.suds_methods.append(suds_method)

    def __getattribute__(self, name):
        """
        Lookup SOAP types and methods first.
        If the attribute is not a SOAP type or method, try to return an attribute of the class.
        """
        if name not in ('suds_types', 'suds_methods') and name in self.suds_types:
            # if the attribute is one of the SOAP types
            return self.suds_client.factory.create(name)
        elif name not in ('suds_types', 'suds_methods') and name in self.suds_methods:
            # if the attribute is one of the SOAP methods
            return self.suds_client.service.__getattr__(name)
        else:
            return super(Client, self).__getattribute__(name)

    def set_header(self):
        """
        Set the header of the SOAP request with the required parameters.
        See page 6 of the Marketo SOAP Api doc.
        """
        authentication_header = self.AuthenticationHeaderInfo
        timestamp = rfc3339(datetime.utcnow(), utc=True, use_system_timezone=False)
        authentication_header.requestSignature = sign(timestamp + self.user_id, self.encryption_key)
        authentication_header.mktowsUserId = self.user_id
        authentication_header.requestTimestamp = timestamp

        self.suds_client.set_options(soapheaders=authentication_header)

    def build_lead_record(self, email=None, attributes=[], marketo_id=None, foreign_person_id=None):
        lead_record = self.LeadRecord
        if marketo_id:
            lead_record.Id = marketo_id
        if foreign_person_id:
            lead_record.ForeignSysPersonId = foreign_person_id
            lead_record.ForeignSysType = 'CUSTOM'
        if email:
            lead_record.Email = email

        if not marketo_id and not foreign_person_id and not email:
            raise InvalidLeadKeyType("No unqiue sync key. Neither email nor foreign_person_id were specified")

        lead_attributes_list = self.ArrayOfAttribute
        for attr in attributes:
            attribute = self.Attribute
            attribute.attrName, attribute.attrType, attribute.attrValue = attr
            lead_attributes_list.attribute.append(attribute)
        lead_record.leadAttributeList = lead_attributes_list
        return lead_record

    def call_service(self, name, *args, **kwargs):
        """Set the header before calling the soap service
        :param name: name of the soap method to call
        :param *args: list of arguments
        :param **kwargs: list of keyword arguments
        """
        self.set_header()
        return self.__getattribute__(name)(*args, **kwargs)

    def get_lead(self, email=None, marketo_id=None):
        """
        :param email: email address of the lead to retry
        :param marketo_id: marketo id of the lead to retry
        :return ResultGetLead
        raise suds.WebFault with code 20103 if not found.
        """
        lead_key = self.LeadKey
        if marketo_id:
            lead_key.keyType = self.LeadKeyRef.IDNUM
            lead_key.keyValue = marketo_id
        elif email:
            lead_key.keyType = self.LeadKeyRef.EMAIL
            lead_key.keyValue = email
        else:
            raise InvalidLeadKeyType('No unique lead key to retrieve')
        return self.call_service('getLead', lead_key)

    def sync_lead(self, email=None, attributes=[], return_lead=False, marketo_id=None, foreign_person_id=None, marketo_cookie=None):
        """
        :param email: email address of the lead to sync
        :param attributes: list of attributes as tuples
            format: ((Name, Type, Value), )
            example: (('FirstName', 'string', 'Sponge'), ('LastName', 'string', 'Bob'))
        :param return_lead: If set to true, complete lead record will be returned. Default: False
        :return ResultSyncLead
        """
        lead_record = self.build_lead_record(email=email, attributes=attributes, marketo_id=marketo_id, foreign_person_id=foreign_person_id)
        return self.call_service('syncLead', lead_record, marketo_cookie=marketo_cookie, return_lead=return_lead)

    def sync_multiple_leads(self, lead_list, dedup_enabled=True):
        """
        :param lead_record_list: List of tuples (email_address, attributes)
        :param dedup_enabled: If set to true, de-duplicate lead record on email address. Default: True
        :return ResultSyncMultipleLeads
        """
        lead_record_list = self.ArrayOfLeadRecord
        for lead in lead_list:
            lead_record_list.leadRecord.append(self.build_lead_record(lead[0], lead[1]))
        return self.call_service('syncMultipleLeads', lead_record_list, dedup_enabled)
