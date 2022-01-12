from typing import List
from dataclasses import dataclass
from nludb.types.base import Request, Model
from nludb.base.base import ApiBase 
from nludb.base.requests import GetRequest

@dataclass
class Space(Model):
  client: ApiBase = None
  id: str = None
  name: str = None
  handle: str = None

  @staticmethod
  def safely_from_dict(d: any, client: ApiBase) -> "Space":
    if 'space' in d:
      d = d['space']

    return Space(
      client = client,
      id = d.get('id', None),
      name = d.get('name', None),
      handle = d.get('handle', None)
    )

  @staticmethod
  def get(
    client: ApiBase,
    id: str = None,
    name: str = None,
    handle: str = None,
    upsert: bool = None,
    spaceId: str = None,
    spaceHandle: str = None,
    space: 'Space' = None
  ) -> "Space":
    req = GetRequest(
      id=id,
      name=name,
      handle=handle,
      upsert=upsert
    )
    return client.post('space/get', req, expect=Space, spaceId=spaceId, spaceHandle=spaceHandle, space=Space)

  @staticmethod
  def create(
    client: ApiBase,
    name: str,
    handle: str,
    externalId: str = None,
    externalType: str = None,
    metadata: any = None,
    upsert: bool = True
  ) -> "Space":
    req = CreateSpace(
      name=name,
      handle=handle,
      upsert=upsert,
      externalId=externalId,
      externalType=externalType,
      metadata=metadata,
    )
    return client.post(
      'space/create', 
      req,
      expect=Space
    )

@dataclass
class CreateSpace(Request):
  id: str = None
  name: str = None
  handle: str = None
  upsert: bool = None
  externalId: str = None
  externalType: str = None
  metadata: str = None

@dataclass
class DeletSpaceRequest(Request):
  spaceId: str

@dataclass
class ListPrivateSpacesRequest(Request):
  pass
