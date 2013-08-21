suds-marketo
============

suds-marketo is a python query client that wraps the Marketo SOAP API. This package is based on https://github.com/segmentio/marketo-python but uses SUDS instead of manual XML requests. Using SUDS makes it easier to update and allows access to unimplemented functions by calling the suds methods directly (client.yourFunction()).

Marketo SOAP Api: https://jira.talendforge.org/secure/attachmentzip/unzip/167201/49761%5B1%5D/Marketo%20Enterprise%20API%202%200.pdf

## Get Started

```
pip install suds-marketo
```

```python
import suds_marketo
client = suds_marketo.Client(soap_endpoint='https://na-q.marketo.com/soap/mktows/2_0',
                        user_id='bigcorp1_461839624B16E06BA2D663',
                        encryption_key='899756834129871744AAEE88DDCC77CDEEDEC1AAAD66')
```

## See available functions and objects

You can see the list of functions and objects available by printing the suds client object.

```python
> print client.suds_types
[ActivityRecord, ActivityType, ActivityTypeFilter, ArrayOfActivityRecord, ArrayOfActivityType,
ArrayOfAttrib, ArrayOfAttribute, ArrayOfBase64Binary, ArrayOfCampaignRecord, ArrayOfCustomObj,
ArrayOfInteger, ArrayOfKeyList, ArrayOfLeadChangeRecord, ArrayOfLeadKey, ArrayOfLeadRecord,
ArrayOfLeadStatus, ArrayOfMObjAssociation, ArrayOfMObjCriteria, ArrayOfMObjFieldMetadata,
ArrayOfMObjStatus, ArrayOfMObject, ArrayOfString, ArrayOfSyncCustomObjStatus, ArrayOfSyncStatus,
ArrayOfVersionedItem, Attrib, Attribute, AuthenticationHeaderInfo, CampaignRecord,
ComparisonEnum, CustomObj, ForeignSysType, ImportToListModeEnum, ImportToListStatusEnum,
LastUpdateAtSelector, LeadActivityList, LeadChangeRecord, LeadKey, LeadKeyRef, LeadKeySelector,
LeadMergeStatusEnum, LeadRecord, LeadSelector, LeadStatus, LeadSyncStatus, ListKey,
ListKeyType, ListOperationType, MObjAssociation, MObjCriteria, MObjFieldMetadata, MObjStatus,
MObjStatusEnum, MObject, MObjectMetadata, MObjectTypeEnum, MergeStatus,
MktowsContextHeaderInfo, ParamsDeleteCustomObjects, ParamsDeleteMObjects,
ParamsDescribeMObject, ParamsGetCampaignsForSource, ParamsGetCustomObjects,
ParamsGetImportToListStatus, ParamsGetLead, ParamsGetLeadActivity, ParamsGetLeadChanges,
ParamsGetMObjects, ParamsGetMultipleLeads, ParamsImportToList, ParamsListMObjects,
ParamsListOperation, ParamsMergeLeads, ParamsRequestCampaign, ParamsScheduleCampaign,
ParamsSyncCustomObjects, ParamsSyncLead, ParamsSyncMObjects, ParamsSyncMultipleLeads,
ReqCampSourceType, ResultDeleteCustomObjects, ResultDeleteMObjects, ResultDescribeMObject,
ResultGetCampaignsForSource, ResultGetCustomObjects, ResultGetImportToListStatus, ResultGetLead,
ResultGetLeadChanges, ResultGetMObjects, ResultGetMultipleLeads, ResultImportToList,
ResultListMObjects, ResultListOperation, ResultMergeLeads, ResultRequestCampaign,
ResultScheduleCampaign, ResultSyncCustomObjects, ResultSyncLead, ResultSyncMObjects,
ResultSyncMultipleLeads, StaticListSelector, StreamPosition, SuccessDeleteCustomObjects,
SuccessDeleteMObjects, SuccessDescribeMObject, SuccessGetCampaignsForSource,
SuccessGetCustomObjects, SuccessGetImportToListStatus, SuccessGetLead, SuccessGetLeadActivity,
SuccessGetLeadChanges, SuccessGetMObjects, SuccessGetMultipleLeads, SuccessImportToList,
SuccessListMObjects, SuccessListOperation, SuccessMergeLeads, SuccessRequestCampaign,
SuccessScheduleCampaign, SuccessSyncCustomObjects, SuccessSyncLead, SuccessSyncMObjects,
SuccessSyncMultipleLeads, SyncCustomObjStatus, SyncOperationEnum, SyncStatus, SyncStatusEnum,
VersionedItem]
> print client.suds_methods
[getCampaignsForSource, deleteCustomObjects, syncMultipleLeads, deleteMObjects, describeMObject,
listOperation, mergeLeads, getCustomObjects, getLead, getImportToListStatus, importToList,
syncLead, getMObjects, getLeadActivity, getLeadChanges, syncMObjects, scheduleCampaign,
listMObjects, syncCustomObjects, requestCampaign, getMultipleLeads]

```

You can access the methods as follow:
```python
> client.getLead(lead_key)
```
You can access the types as follow:
```python
> client.LeadKey # Simple type
> client.LeadKeyRef.EMAIL # Enumeration
```

## Call functions

If the function is defined in the client class:
```python
> lead = client.get_lead('user@gmail.com')
```

If the function you are looking for is not defined in the client class:

```python
> lead_key = client.LeadKey # You need to create the proper object to pass to the function
> lead_key.keyType = client.LeadKeyRef.EMAIL
> lead_key.keyValue = 'test@punchtab.com'
> client.set_header() # You need to sign the header every time you make a call to the SOAP Api
> resp = client.getLead(lead_key)
```

### Error

An Exception is raised if a Marketo error occurs (caused either by client or server).

```python
> from suds import WebFault
> try:
>    lead = client.get_lead('test@punchtab.com')
> except WebFault as e:
>    print e

Server raised fault: '20103 - Lead not found'
```

As described in the Appendix B of the Marketo API, you can access the following error attributes:
```
> print e.fault.faultcode
SOAP-ENV:Client

> print e.fault.faultstring
20103 - Lead not found

> print e.fault.detail
(detail){
   serviceException = 
      (serviceException){
         name = "mktServiceException"
         message = "No lead found with EMAIL = test@punchtab.com (20103)"
         code = "20103"
      }
 }

> print e.fault.detail.serviceException
(serviceException){
   name = "mktServiceException"
   message = "No lead found with EMAIL = test@punchtab.com (20103)"
   code = "20103"
 }

> print e.fault.detail.serviceException.name
mktServiceException

> print e.fault.detail.serviceException.message
No lead found with EMAIL = test@punchtab.com (20103)

> print e.fault.detail.serviceException.code
20103
```

### License

The MIT License (MIT)

Copyright (c) 2013 PunchTab, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
