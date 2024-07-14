import json
import re
from dataclasses import dataclass


@dataclass
class DXCCEntity:
    name: str
    flag: str
    prefixes: list[str]
    prefix_regex: re.Pattern
    country_code: str
    deleted: bool


class DXCCRepository:
    def __init__(self) -> None:
        self._repo: list[DXCCEntity] = []

    def append(self, entity: DXCCEntity):
        self._repo.append(entity)

    def get_entity_for_callsign(self, callsign: str) -> DXCCEntity:
        for entity in self._repo:
            if not entity.prefix_regex:
                continue
            matches = entity.prefix_regex.match(callsign)
            if matches:
                return entity


dxcc_entities = DXCCRepository()

with open("dxcc-json/dxcc.json", "r", encoding="utf8") as dxccjson:
    parsed = json.load(dxccjson)

    root = parsed["dxcc"]
    for entry in root:
        flag = entry["flag"]
        name = entry["name"]
        prefixes = entry["prefix"].split(",")
        prefix_regex_str = entry["prefixRegex"]
        prefix_regex = re.compile(prefix_regex_str) if prefix_regex_str else None
        country_code = entry["countryCode"]
        deleted = entry["deleted"]

        if not deleted:
            dxcc_entities.append(
                DXCCEntity(name, flag, prefixes, prefix_regex, country_code, deleted)
            )
