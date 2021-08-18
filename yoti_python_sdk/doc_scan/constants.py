# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from enum import Enum


ID_DOCUMENT_AUTHENTICITY = "ID_DOCUMENT_AUTHENTICITY"
ID_DOCUMENT_COMPARISON = "ID_DOCUMENT_COMPARISON"
ID_DOCUMENT_TEXT_DATA_CHECK = "ID_DOCUMENT_TEXT_DATA_CHECK"
ID_DOCUMENT_TEXT_DATA_EXTRACTION = "ID_DOCUMENT_TEXT_DATA_EXTRACTION"
ID_DOCUMENT_FACE_MATCH = "ID_DOCUMENT_FACE_MATCH"
LIVENESS = "LIVENESS"
ZOOM = "ZOOM"
SUPPLEMENTARY_DOCUMENT_TEXT_DATA_CHECK = "SUPPLEMENTARY_DOCUMENT_TEXT_DATA_CHECK"
SUPPLEMENTARY_DOCUMENT_TEXT_DATA_EXTRACTION = (
    "SUPPLEMENTARY_DOCUMENT_TEXT_DATA_EXTRACTION"
)

CAMERA = "CAMERA"
CAMERA_AND_UPLOAD = "CAMERA_AND_UPLOAD"

RESOURCE_UPDATE = "RESOURCE_UPDATE"
TASK_COMPLETION = "TASK_COMPLETION"
CHECK_COMPLETION = "CHECK_COMPLETION"
SESSION_COMPLETION = "SESSION_COMPLETION"

ID_DOCUMENT = "ID_DOCUMENT"
SUPPLEMENTARY_DOCUMENT = "SUPPLEMENTARY_DOCUMENT"
ORTHOGONAL_RESTRICTIONS = "ORTHOGONAL_RESTRICTIONS"
DOCUMENT_RESTRICTIONS = "DOCUMENT_RESTRICTIONS"
INCLUSION_WHITELIST = "WHITELIST"
INCLUSION_BLACKLIST = "BLACKLIST"

ALWAYS = "ALWAYS"
FALLBACK = "FALLBACK"
NEVER = "NEVER"

DESIRED = "DESIRED"
IGNORE = "IGNORE"

PROOF_OF_ADDRESS = "PROOF_OF_ADDRESS"


class DocScanAuthType(Enum):
    BASIC = 'BASIC'
    BEARER = 'BEARER'
