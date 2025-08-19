from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class GroupModel(BaseModel):
    groupId: str
    pageRange: List[int]
    language: str
    isTranslationRequired: bool
    translatedText: Optional[str] = None
    originalText: str
    summaryOriginalLanguage: Optional[str] = None
    summaryTranslatedEnglish: Optional[str] = None
    docTypeCode: str
    docTypeDescription: str
    assumed: bool
    regulatoryRiskFlags: List[str]
    metadataSummary: Dict[str, Any]
    confidenceScores: Dict[str, float]
    aiReasoning: str

class ProcessResponse(BaseModel):
    detectedMimeType: str
    isValidMimeType: bool
    routingDecision: str
    mimeConfidence: float
    groups: List[GroupModel]
    downloadZip: Optional[str] = None
