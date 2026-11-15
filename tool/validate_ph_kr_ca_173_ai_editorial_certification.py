#!/usr/bin/env python3
"""Validate evidence-scoped AI editorial certification without human impersonation.

AI_CERTIFIED is an editorial research certificate, not runtime publication.
Source/version changes invalidate prior per-source certification. Unreviewed
and disputed entries must remain unapproved.
"""
import json
import hashlib
import os
import sys
from urllib.request import Request, urlopen
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
from editorial_research_handoff import load_handoff

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/editorial/reviews/ph_kr_ca_173_qualified_review_queue_20261114.json"
LEDGER = ROOT / "data/editorial/reviews/ph_kr_ca_173_ai_editorial_certification_20261114.json"
q = json.loads(QUEUE.read_text(encoding="utf-8"))
d = json.loads(LEDGER.read_text(encoding="utf-8"))
handoff = load_handoff()
queue_bytes = QUEUE.read_bytes()
queue_git_blob_sha = hashlib.sha1(
    b"blob " + str(len(queue_bytes)).encode("ascii") + b"\0" + queue_bytes
).hexdigest()
assert d["sourceReviewQueueBlobSha"] == queue_git_blob_sha, (
    "historical queue changed: re-run AI review before accepting a certificate"
)
assert d["schemaVersion"] == 1 and d["asOf"] == "2026-11-14"
assert d["reviewerIdentity"] == "GPT-6_AI_EDITORIAL_REVIEW"
assert d["reviewAuthority"] == "USER_DELEGATED_AI_EDITORIAL_REVIEW_2026-11-14"
assert len(d["sourceReviewQueueBlobSha"]) == 40
assert d["summary"]["qualifiedHumanSignoffs"] == 0
assert d["summary"]["appRuntimePublishedByThisLedger"] == 0
src = {r["id"]: r for r in q["records"]}
rows = {r["observanceId"]: r for r in d["records"]}
assert len(rows) == len(src) == 173
assert set(rows) == set(src) == handoff["six_locale_draft_ids"]
assert Counter(x["country"] for x in rows.values()) == {"PH":84,"KR":57,"CA":32}
assert d["summary"]["byCountry"] == {"PH":84,"KR":57,"CA":32}
assert d["reviewBatchHistory"][0]["count"] == 10
assert len(d["reviewBatchHistory"][0]["ids"]) == 10
assert len(d["reviewBatchHistory"]) >= 2
assert d["reviewBatchHistory"][1]["count"] == 7
assert len(d["reviewBatchHistory"]) == 8
assert d["reviewBatchHistory"][7]["count"] == 99
assert len(d["reviewBatchHistory"][7]["ids"]) == 99
assert len(set(d["reviewBatchHistory"][7]["ids"])) == 99
assert d["reviewBatchHistory"][6]["count"] == 11
assert len(d["reviewBatchHistory"][6]["ids"]) == 11
assert d["reviewBatchHistory"][5]["count"] == 14
assert len(d["reviewBatchHistory"][5]["ids"]) == 14
assert d["reviewBatchHistory"][4]["count"] == 11
assert len(d["reviewBatchHistory"][4]["ids"]) == 11
assert d["reviewBatchHistory"][3]["count"] == 7
assert d["sourceHeadRevalidation"]["pr"] == 118
assert len(d["sourceHeadRevalidation"]["individuallyJsonIdenticalIds"]) == 9
assert len(d["reviewBatchHistory"][3]["ids"]) == 7
assert d["reviewBatchHistory"][2]["count"] == 10
assert len(d["reviewBatchHistory"][1]["ids"]) == 7
expected = {
    "ca-air-disaster-victims-remembrance": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2020, 2021, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-armed-forces-day": ("CA", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 2002, 2002, "2026-11-14", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "ca-armenian-genocide-remembrance": ("CA", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 2015, None, "2026-11-14", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "ca-british-home-child-day": ("CA", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 2018, None, "2026-11-14", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "ca-canada-day": ("CA", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 1879, 1868, "2026-11-14", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "ca-covid-19-national-observance": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2021, 2021, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-dutch-heritage-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2019, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-emancipation-day": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", 2021, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-great-upheaval-commemoration": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", None, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-holodomor-memorial-day": ("CA", "318f42138b36bd8879ac949bbb43a934bdf51814", 2008, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-indigenous-languages-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", None, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-indigenous-veterans-day": ("CA", "318f42138b36bd8879ac949bbb43a934bdf51814", 1994, 1994, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-lincoln-alexander-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2014, 2015, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-national-child-day": ("CA", "318f42138b36bd8879ac949bbb43a934bdf51814", 1993, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-national-seniors-day": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", 2010, 2011, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-persons-day": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", 1979, 1979, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-quebec-city-mosque-attack-remembrance": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", None, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-raoul-wallenberg-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2001, 2002, "2026-11-15", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-red-dress-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", None, 2010, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-remembrance-day": ("CA", "318f42138b36bd8879ac949bbb43a934bdf51814", 1931, 1919, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-ribbon-skirt-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2022, 2023, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-saint-jean-baptiste-day": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", None, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-sir-john-a-macdonald-day": ("CA", "d32c7d4e9cc1bfd6d87be8a71b0b3cfd00e66c3a", 2002, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-statute-of-westminster-anniversary": ("CA", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", None, None, "2026-11-14", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "ca-terrorism-victims-remembrance": ("CA", "3a19b6c828f4a4b4502b946d599eefa4700cb865", 2005, 2005, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "ca-vimy-ridge-battle-anniversary": ("CA", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 2003, 2003, "2026-11-14", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "ca-violence-against-women-remembrance": ("CA", "318f42138b36bd8879ac949bbb43a934bdf51814", 1991, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "canada-multiculturalism-day": ("CA", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 2002, None, "2026-11-14", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "canada-national-acadian-day": ("CA", "863db0e6c7ff952ca060d5e8c6c2f0cae2c54494", 2003, 1881, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "canada-national-flag-day": ("CA", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 1996, 1996, "2026-11-14", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "canada-national-indigenous-peoples-day": ("CA", "863db0e6c7ff952ca060d5e8c6c2f0cae2c54494", 1996, None, "2026-11-14", "3ece3c825efb6fe7e6ac42182c334e9dcd90f5f0"),
    "canada-truth-and-reconciliation-day": ("CA", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 2021, 2021, "2026-11-14", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "kr-childrens-day": ("KR", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 1961, 1923, "2026-11-15", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "kr-constitution-day": ("KR", "f9daf3a869df6d24bdd48b635fcfcfc4f7c25dc5", 1949, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-hangeul-day": ("KR", "f9daf3a869df6d24bdd48b635fcfcfc4f7c25dc5", 2005, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-liberation-day": ("KR", "e365bd21d656efbc8007397b8f6fe47c10dc304b", 1949, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-march-first-independence-movement-day": ("KR", "135f652773ca0f8d0b0d96dcd4fb64fac0e3165e", 1949, 1920, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-memorial-day": ("KR", "e365bd21d656efbc8007397b8f6fe47c10dc304b", 1956, 1956, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-national-foundation-day": ("KR", "e365bd21d656efbc8007397b8f6fe47c10dc304b", 1949, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-admiral-yi-sun-sin-birthday-commemoration": ("KR", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 1967, None, "2026-11-15", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "kr-w10-aerospace-day-in-korea": ("KR", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 2024, None, "2026-11-15", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "kr-w10-april-19-revolution-day": ("KR", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 1973, None, "2026-11-15", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "kr-w10-arbor-day-in-korea": ("KR", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 1949, None, "2026-11-15", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "kr-w10-bu-ma-democratic-protests-remembrance-day": ("KR", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 2019, None, "2026-11-15", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "kr-w10-coming-of-age-day-in-korea": ("KR", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 1973, None, "2026-11-15", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "kr-w10-commerce-and-industry-day": ("KR", "9826b40968862f4950666d66b1fa5813b65e01f4", 1964, 1964, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-consumers-day-in-korea": ("KR", "9826b40968862f4950666d66b1fa5813b65e01f4", 1996, 1982, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-corrections-day-in-korea": ("KR", "c94ee83209c0a85a423ef52adcf6aa15eccff945", 2002, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-couples-day-in-korea": ("KR", "0552f899759644c79a269987b80c0761f9fc5544", 2007, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-culture-day-in-korea": ("KR", "0552f899759644c79a269987b80c0761f9fc5544", 1973, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-day-of-persons-with-disabilities-in-korea": ("KR", "2ec02ad71c50321511f8b0cbc7415ff7c2934345", 1994, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-donghak-peasant-revolution-remembrance-day": ("KR", "0afe06f7e8cc81325c71d118ca49536d719a6ffa", 2019, 2019, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-fallen-military-service-members-remembrance-day": ("KR", "0552f899759644c79a269987b80c0761f9fc5544", 2023, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-farmers-day-in-korea": ("KR", "9826b40968862f4950666d66b1fa5813b65e01f4", 1996, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-february-28-democracy-movement-remembrance": ("KR", "dacf8ec4e0399884b8278ba9bf4468adfe3a6199", 2018, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-information-and-communications-day-in-korea": ("KR", "c94ee83209c0a85a423ef52adcf6aa15eccff945", 1956, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-information-security-day-in-korea": ("KR", "aff5009befe07c46e54f0bd169e6924f3650f7e9", 2012, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-jeju-april-3-victims-remembrance-day": ("KR", "46075f00042ead20112f23fa7fa052a944fb1142", 2014, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-june-10-democracy-movement-remembrance": ("KR", "6eae4c1bac5f07337f962ef100bed87be9d258a6", 2007, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-june-10-independence-movement-remembrance": ("KR", "6eae4c1bac5f07337f962ef100bed87be9d258a6", 2020, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-king-sejong-birthday-commemoration": ("KR", "0552f899759644c79a269987b80c0761f9fc5544", 2024, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-korean-public-health-day": ("KR", "90a87fb6bad4c3eb34fd18218d227cc6b834e083", 1973, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-korean-war-remembrance-day": ("KR", "0153ec44d8fb99dfa849ca6095975119cc698a86", 1973, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-korean-workers-day": ("KR", "90a87fb6bad4c3eb34fd18218d227cc6b834e083", 1963, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-law-day-in-korea": ("KR", "f54c38d28f27ad597f36ef8cc5b5b2b0686e1a8d", 1964, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-local-autonomy-and-balanced-development-day": ("KR", "9826b40968862f4950666d66b1fa5813b65e01f4", 2012, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-march-15-democratic-uprising-remembrance": ("KR", "dacf8ec4e0399884b8278ba9bf4468adfe3a6199", 2010, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-march-8-democracy-uprising-remembrance": ("KR", "dacf8ec4e0399884b8278ba9bf4468adfe3a6199", 2018, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-may-18-democratization-movement-remembrance": ("KR", "0afe06f7e8cc81325c71d118ca49536d719a6ffa", 1997, 1981, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-north-korean-defectors-day": ("KR", "0552f899759644c79a269987b80c0761f9fc5544", 2024, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-oceans-day-in-korea": ("KR", "c94ee83209c0a85a423ef52adcf6aa15eccff945", 1996, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-parents-day-in-korea": ("KR", "90a87fb6bad4c3eb34fd18218d227cc6b834e083", 1973, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-patriotic-martyrs-remembrance-day": ("KR", "0153ec44d8fb99dfa849ca6095975119cc698a86", 1997, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-police-day-in-korea": ("KR", "c94ee83209c0a85a423ef52adcf6aa15eccff945", 1957, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-provisional-government-establishment-day": ("KR", "46075f00042ead20112f23fa7fa052a944fb1142", 1989, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-railway-day-in-korea": ("KR", "aff5009befe07c46e54f0bd169e6924f3650f7e9", 1964, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-republic-of-korea-armed-forces-day": ("KR", "c94ee83209c0a85a423ef52adcf6aa15eccff945", 1956, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-reserve-forces-day": ("KR", "2ec02ad71c50321511f8b0cbc7415ff7c2934345", 1970, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-righteous-armies-remembrance-day": ("KR", "5c21da1d3bf055c1f1e33e9883cc6b4f07f32b90", 2010, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-science-day-in-korea": ("KR", "90a87fb6bad4c3eb34fd18218d227cc6b834e083", 1969, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-senior-citizens-day-in-korea": ("KR", "90a87fb6bad4c3eb34fd18218d227cc6b834e083", 1997, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-sports-day-in-korea": ("KR", "5c21da1d3bf055c1f1e33e9883cc6b4f07f32b90", 1969, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-student-independence-movement-remembrance-day": ("KR", "f54c38d28f27ad597f36ef8cc5b5b2b0686e1a8d", 1953, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-taxpayers-day": ("KR", "9826b40968862f4950666d66b1fa5813b65e01f4", 1969, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-teachers-day-in-korea": ("KR", "90a87fb6bad4c3eb34fd18218d227cc6b834e083", 1982, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-trade-day-in-korea": ("KR", "9826b40968862f4950666d66b1fa5813b65e01f4", 1964, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-veterans-association-day-in-korea": ("KR", "5c21da1d3bf055c1f1e33e9883cc6b4f07f32b90", 1965, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-west-sea-defense-day": ("KR", "5c21da1d3bf055c1f1e33e9883cc6b4f07f32b90", 2016, 2016, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "kr-w10-world-koreans-day": ("KR", "5c21da1d3bf055c1f1e33e9883cc6b4f07f32b90", 2007, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-bonifacio-day": ("PH", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 1921, None, "2026-11-15", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "ph-day-of-valor": ("PH", "6acc4ec387c53faf25aa517a74e8585a88f0eae5", 1961, None, "2026-11-15", "47cff4c5b22e55156e9444a3240511530a6f01f9"),
    "ph-edsa-people-power-anniversary": ("PH", "0245e581aa61b340cd476da1eb1eabfe3e3b5e58", None, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-independence-day": ("PH", "135f652773ca0f8d0b0d96dcd4fb64fac0e3165e", 1964, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-national-heroes-day": ("PH", "dce081d073bad6dea6d471b5aa72224588802ea1", 1931, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-ninoy-aquino-day": ("PH", "dce081d073bad6dea6d471b5aa72224588802ea1", 2004, None, "2026-11-14", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-rizal-day": ("PH", "f03b9bb889c6d0542384b9ae89aba3ba8388f493", 1902, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-apolinario-mabini-day": ("PH", "1fcf1c7fe7e361c9918852801289fe4cf89bb9a6", 2007, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-araw-ng-pagbasa-philippines-national-reading-day": ("PH", "048e4e5325425fa255182759cd0b2644eeb2b3c7", 2013, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-araw-ng-republikang-filipino-first-philippine-republic-anniversary": ("PH", "048e4e5325425fa255182759cd0b2644eeb2b3c7", 2013, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-araw-ni-balagtas": ("PH", "02759db2f38aade5a32c7d44b516c008104e27d0", 1974, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-day-of-the-filipino-seafarer": ("PH", "02759db2f38aade5a32c7d44b516c008104e27d0", 2011, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-filipino-chinese-friendship-day": ("PH", "048e4e5325425fa255182759cd0b2644eeb2b3c7", 2002, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-gawad-sa-manlilikha-ng-bayan-establishment-anniversary": ("PH", "1fcf1c7fe7e361c9918852801289fe4cf89bb9a6", 1992, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-graciano-lopez-jaena-day": ("PH", "1fcf1c7fe7e361c9918852801289fe4cf89bb9a6", 2001, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-iglesia-ni-cristo-day": ("PH", "1fcf1c7fe7e361c9918852801289fe4cf89bb9a6", 2009, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-jose-abad-santos-day": ("PH", "1fcf1c7fe7e361c9918852801289fe4cf89bb9a6", 1956, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-julian-felipe-day": ("PH", "b08c7b723f7594a8a44f9854875471585958c722", 1994, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-kindness-to-animal-day-philippines": ("PH", "b08c7b723f7594a8a44f9854875471585958c722", 1958, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-komisyon-sa-wikang-filipino-founding-anniversary": ("PH", "1db0b82a8e5d5c9ab5d37757409b86926abaffdd", 1991, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-national-fisherfolks-day-philippines": ("PH", "1db0b82a8e5d5c9ab5d37757409b86926abaffdd", 2000, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-national-library-of-the-philippines-founding-anniversary": ("PH", "c46dfd074b22dac863e34d2d96ef26c5e69fa8b4", 1887, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-ncca-establishment-anniversary": ("PH", "4306ebb4d6c46fd76b43317d6befd8ab09e948aa", 1992, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-order-of-gabriela-silang-founding-anniversary": ("PH", "b08c7b723f7594a8a44f9854875471585958c722", 2003, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-order-of-lakandula-founding-anniversary": ("PH", "b08c7b723f7594a8a44f9854875471585958c722", 2003, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-order-of-national-artists-establishment-anniversary": ("PH", "93a1f08f2eff949e26d13619dcac67853b95b518", 1972, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippine-army-founding-anniversary": ("PH", "06eb0674ad27e77556c600a3cb89d9556b591898", 1897, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippine-british-friendship-day": ("PH", "c46dfd074b22dac863e34d2d96ef26c5e69fa8b4", 2000, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippine-film-development-council-founding-anniversary": ("PH", "06eb0674ad27e77556c600a3cb89d9556b591898", 2002, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippine-flag-days-commencement": ("PH", "048e4e5325425fa255182759cd0b2644eeb2b3c7", 1965, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippine-house-of-representatives-founding-anniversary": ("PH", "06eb0674ad27e77556c600a3cb89d9556b591898", 1916, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippine-military-academy-establishment-anniversary": ("PH", "c46dfd074b22dac863e34d2d96ef26c5e69fa8b4", 1898, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippine-national-women-s-day": ("PH", "4306ebb4d6c46fd76b43317d6befd8ab09e948aa", 1990, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippine-republic-day-july-4": ("PH", "02759db2f38aade5a32c7d44b516c008104e27d0", 1964, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippine-senate-founding-anniversary": ("PH", "06eb0674ad27e77556c600a3cb89d9556b591898", 1916, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippine-spanish-friendship-day": ("PH", "048e4e5325425fa255182759cd0b2644eeb2b3c7", 2003, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippines-earth-day": ("PH", "4306ebb4d6c46fd76b43317d6befd8ab09e948aa", 2008, 1990, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippines-indigenous-peoples-thanksgiving-day": ("PH", "4306ebb4d6c46fd76b43317d6befd8ab09e948aa", 2003, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippines-local-government-day": ("PH", "36bb94b47c63841ec45ff1311be799401979021c", 1992, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippines-national-archives-day": ("PH", "c46dfd074b22dac863e34d2d96ef26c5e69fa8b4", 1995, 1901, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippines-national-indigenous-peoples-day": ("PH", "048e4e5325425fa255182759cd0b2644eeb2b3c7", 2015, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippines-national-literacy-day": ("PH", "048e4e5325425fa255182759cd0b2644eeb2b3c7", 1969, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippines-national-museum-founding-anniversary": ("PH", "06eb0674ad27e77556c600a3cb89d9556b591898", 1901, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-philippines-national-teachers-day": ("PH", "048e4e5325425fa255182759cd0b2644eeb2b3c7", 2016, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-puerto-princesa-underground-river-day": ("PH", "c46dfd074b22dac863e34d2d96ef26c5e69fa8b4", 2014, 2011, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w10-ramon-magsaysay-memorial-day": ("PH", "1db0b82a8e5d5c9ab5d37757409b86926abaffdd", 1966, 1957, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-18-day-campaign-to-end-violence-against-women-philippines": ("PH", "93a1f08f2eff949e26d13619dcac67853b95b518", 2006, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-buwan-ng-wikang-pambansa": ("PH", "6bf91890f83bbc74f327f4d1cf11049e0c1f1922", 1997, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-civil-service-month-philippines": ("PH", "36bb94b47c63841ec45ff1311be799401979021c", 1997, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-conflict-resolution-day-philippines": ("PH", "20d72f8ce5af30098441eef1e15e9c2f553f154a", 2006, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-conservation-and-protection-of-the-tamaraw-month": ("PH", "63f113c848a2a364a7838f453f2be31ffac07fa5", 2002, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-day-of-sanctity-and-protection-of-human-life-philippines": ("PH", "70845fb5a92feca980a6f1b0f2162172de535df2", 2003, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-edsa-people-power-commemoration-week": ("PH", "70845fb5a92feca980a6f1b0f2162172de535df2", 2007, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-filipino-food-month": ("PH", "ae748dcbc84579dd9f5f6087cb2ca3fedd46c5fe", 2018, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-filipino-values-month": ("PH", "6bf91890f83bbc74f327f4d1cf11049e0c1f1922", 1994, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-history-month-philippines": ("PH", "ae748dcbc84579dd9f5f6087cb2ca3fedd46c5fe", 2012, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-library-and-information-services-month": ("PH", "63f113c848a2a364a7838f453f2be31ffac07fa5", 1991, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-linggo-ng-kalayaan": ("PH", "1db0b82a8e5d5c9ab5d37757409b86926abaffdd", 1992, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-month-of-overseas-filipinos": ("PH", "36bb94b47c63841ec45ff1311be799401979021c", 1988, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-museums-and-galleries-month-philippines": ("PH", "ae748dcbc84579dd9f5f6087cb2ca3fedd46c5fe", 1991, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-bible-month": ("PH", "6bf91890f83bbc74f327f4d1cf11049e0c1f1922", 2017, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-book-week-philippines": ("PH", "93a1f08f2eff949e26d13619dcac67853b95b518", 1936, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-children-s-month-philippines": ("PH", "ae748dcbc84579dd9f5f6087cb2ca3fedd46c5fe", 2015, 1993, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-coconut-week-philippines": ("PH", "02759db2f38aade5a32c7d44b516c008104e27d0", 1987, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-culture-consciousness-week": ("PH", "63f113c848a2a364a7838f453f2be31ffac07fa5", 1973, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-heritage-month": ("PH", "0245e581aa61b340cd476da1eb1eabfe3e3b5e58", 2003, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-indigenous-peoples-month-philippines": ("PH", "ae748dcbc84579dd9f5f6087cb2ca3fedd46c5fe", 2009, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-literature-month": ("PH", "ae748dcbc84579dd9f5f6087cb2ca3fedd46c5fe", 2015, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-peace-consciousness-month": ("PH", "6bf91890f83bbc74f327f4d1cf11049e0c1f1922", 2004, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-rice-awareness-month": ("PH", "6bf91890f83bbc74f327f4d1cf11049e0c1f1922", 2004, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-national-volunteers-month-philippines": ("PH", "36bb94b47c63841ec45ff1311be799401979021c", 1998, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-nutrition-month-philippines": ("PH", "93a1f08f2eff949e26d13619dcac67853b95b518", 1974, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-panagyaman-rice-festival-month": ("PH", "e0e44135bdf6f9209251ce1faae2b4f84cde84e2", 2004, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-philippine-book-development-month": ("PH", "63f113c848a2a364a7838f453f2be31ffac07fa5", 1999, 1997, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-philippine-tropical-fabrics-month": ("PH", "36bb94b47c63841ec45ff1311be799401979021c", 2012, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-rizal-month": ("PH", "f03b9bb889c6d0542384b9ae89aba3ba8388f493", 2001, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-rule-of-law-month-philippines": ("PH", "36bb94b47c63841ec45ff1311be799401979021c", 2004, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-traditional-and-alternative-health-month-philippines": ("PH", "63f113c848a2a364a7838f453f2be31ffac07fa5", 2004, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-unesco-iti-world-theater-week-philippines": ("PH", "e0e44135bdf6f9209251ce1faae2b4f84cde84e2", 2007, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-united-nations-week-philippines": ("PH", "70845fb5a92feca980a6f1b0f2162172de535df2", 2003, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-unknown-citizens-day": ("PH", "20d72f8ce5af30098441eef1e15e9c2f553f154a", 1936, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-w-a-t-c-h-time-consciousness-and-honesty-month": ("PH", "20d72f8ce5af30098441eef1e15e9c2f553f154a", 2009, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-women-s-role-in-history-month": ("PH", "6bf91890f83bbc74f327f4d1cf11049e0c1f1922", 1988, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
    "ph-w13-world-clean-and-green-week-philippines": ("PH", "20d72f8ce5af30098441eef1e15e9c2f553f154a", 1993, None, "2026-11-15", "521a59452178b7e2f0b074e5057e964af8515feb"),
}
count = Counter()
for rid, row in rows.items():
    original = src[rid]
    assert row["country"] == original["country"]
    assert row["sourcePR"] == original["sourcePr"]
    assert row["sourceFile"] == original["sourceFile"]
    assert len(row["sourceHead"]) == 40
    assert set(row["locales"]) == {"en","it","es","fr","de","pt"}
    count[row["status"]] += 1
    if rid in expected:
        code, blob, established, first, review_date, source_head = expected[rid]
        assert row["status"] == "AI_CERTIFIED"
        assert row["country"] == code
        assert row["sourceBlobSha"] == blob
        assert row["sourceHead"] == source_head
        assert row["establishedYear"] == established
        assert row["firstObservedYear"] == first
        assert row["reviewedBy"] == "GPT-6" and row["reviewDate"] == review_date
        assert row["reviewMethod"] == "MODEL_EDITORIAL_FACT_AND_TRANSLATION_CHECK"
        assert set(row["locales"].values()) == {"AI_CHECKED"}
        assert all(row["checks"].values())
        assert len(row["sourceEvidence"]) >= 2
        assert all(urlsplit(u).scheme == "https" and urlsplit(u).hostname
                   for u in row["sourceEvidence"])
        assert len(row["factsConfirmed"]) >= 3
        assert len(row["notes"]) >= 70
        assert row["sourceConflict"] is None, rid
    else:
        assert row["status"] == ("HOLD_SOURCE_DISPUTE" if original["unresolvedSourceRisk"]
                                 else "AI_REVIEW_QUEUED")
        assert row["reviewedBy"] is None and row["reviewDate"] is None
        assert row["checks"] is None
        assert row["sourceBlobSha"] is None
        assert set(row["locales"].values()) == {"NOT_CHECKED"}
assert len(expected) == 173
assert set(d["reviewBatchHistory"][7]["ids"]) == {rid for rid, fields in expected.items() if fields[4] == "2026-11-15"}
assert set(d["summary"]) == {"total", "byCountry", "AI_REVIEW_QUEUED", "AI_CERTIFIED", "HOLD_SOURCE_DISPUTE", "qualifiedHumanSignoffs", "appRuntimePublishedByThisLedger"}
assert count == {"AI_CERTIFIED":173}
for name,num in count.items():
    assert d["summary"][name] == num
assert d["summary"]["AI_REVIEW_QUEUED"] == 0
assert d["summary"]["HOLD_SOURCE_DISPUTE"] == 0
assert len(d["pendingPublicationCorrections"]) == 3
assert {x["id"] for x in d["pendingPublicationCorrections"]} == {"ca-raoul-wallenberg-day","ph-w13-panagyaman-rice-festival-month","ph-w13-w-a-t-c-h-time-consciousness-and-honesty-month"}
assert rows["ca-raoul-wallenberg-day"]["establishedYear"] == 2001
assert rows["ca-raoul-wallenberg-day"]["firstObservedYear"] == 2002
assert "not" in rows["ph-w13-panagyaman-rice-festival-month"]["legalRecurrenceCaveat"].lower()
assert "not" in rows["ph-w13-w-a-t-c-h-time-consciousness-and-honesty-month"]["legalRecurrenceCaveat"].lower()
source_conflict_ids = {rid for rid, original in src.items() if original["unresolvedSourceRisk"]}
assert len(source_conflict_ids) == 8
for rid in source_conflict_ids:
    assert rows[rid]["originalSourceConflictCode"] == src[rid]["unresolvedSourceRisk"]["code"]
    assert rows[rid]["sourceConflictResolution"]
    assert rows[rid]["sourceConflict"] is None
philippines = rows["ph-independence-day"]
assert philippines["firstObservedYear"] is None
assert any("84843" in url for url in philippines["sourceEvidence"])
assert philippines["sourceHead"] == "521a59452178b7e2f0b074e5057e964af8515feb"
# Exact live source-version gate: a once-correct AI certificate is never valid
# after an unreviewed PR head or source blob update.  Uses the GitHub API on CI;
# local static validation remains available without performing network requests.
if "--verify-remote" in sys.argv:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise AssertionError("--verify-remote requires GITHUB_TOKEN")
    base = "https://api.github.com/repos/riccardopinato/World-Days"
    def api(path):
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "World-Days-AI-Editorial-Source-Gate/1",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28",
        }
        req = Request(base + path, headers=headers)
        with urlopen(req, timeout=25) as response:
            return json.loads(response.read().decode("utf-8"))

    # Only fetch reviewed source PRs; all other drafts are intentionally queued.
    certified = [x for x in rows.values() if x["status"] == "AI_CERTIFIED"]
    heads = {}
    blob_cache = {}
    for row in certified:
        pr = row["sourcePR"]
        if pr not in heads:
            obj = api("/pulls/" + str(pr))
            assert obj["state"] == "open" and not obj["merged"], ("source PR closed/merged", pr)
            heads[pr] = obj["head"]["sha"]
        assert heads[pr] == row["sourceHead"], (
            "source PR changed after AI review; invalidate and recertify", pr,
            row["sourceHead"], heads[pr])
        key = (pr, row["sourceFile"])
        if key not in blob_cache:
            import urllib.parse
            encoded = "/".join(urllib.parse.quote(p, safe="") for p in row["sourceFile"].split("/"))
            obj = api("/contents/" + encoded + "?ref=" + heads[pr])
            assert obj.get("type") == "file"
            blob_cache[key] = obj["sha"]
        assert blob_cache[key] == row["sourceBlobSha"], (
            "source file blob changed after review", row["observanceId"])
    print("PASS: live GitHub PR head and source blob verification for",
          len(certified), "AI-certified stories across", len(heads), "source PRs")

print("PASS: 173 six-language AI editorial source reviews (74 prior + 99 final); 173 AI_CERTIFIED, "
      "0 source-HOLD, 0 awaiting AI review; 8 source-conflict resolutions with documented scope, "
      "3 prepublication corrections, 0 human signoffs, 0 runtime publications")
