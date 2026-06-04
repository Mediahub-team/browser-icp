"""Тонкие обёртки сервисов Yandex Direct API v5 поверх DirectClient.call().

Каждый метод — это {Service}.{method}. Параметры передаём как dict по справочнику API.
Документация методов: https://yandex.ru/dev/direct/doc/ref-v5/<service>/<method>.html
"""
from __future__ import annotations


class Services:
    def __init__(self, client):
        self.c = client

    # --- Кампании ---
    def campaigns_add(self, campaigns):
        return self.c.call("campaigns", "add", {"Campaigns": campaigns})

    def campaigns_get(self, field_names=None, selection=None):
        params = {"FieldNames": field_names or ["Id", "Name", "Type", "State", "Status"]}
        if selection:
            params["SelectionCriteria"] = selection
        else:
            params["SelectionCriteria"] = {}
        return self.c.call("campaigns", "get", params)

    def campaigns_suspend(self, ids):
        return self.c.call("campaigns", "suspend", {"SelectionCriteria": {"Ids": ids}})

    # --- Группы объявлений ---
    def adgroups_add(self, adgroups):
        return self.c.call("adgroups", "add", {"AdGroups": adgroups})

    def adgroups_get(self, campaign_ids, field_names=None):
        return self.c.call("adgroups", "get", {
            "SelectionCriteria": {"CampaignIds": campaign_ids},
            "FieldNames": field_names or ["Id", "Name", "CampaignId"],
        })

    # --- Объявления ---
    def ads_add(self, ads):
        return self.c.call("ads", "add", {"Ads": ads})

    def ads_get(self, campaign_ids, field_names=None):
        return self.c.call("ads", "get", {
            "SelectionCriteria": {"CampaignIds": campaign_ids},
            "FieldNames": field_names or ["Id", "AdGroupId", "State", "Status", "Type"],
        })

    def ads_moderate(self, ids):
        return self.c.call("ads", "moderate", {"SelectionCriteria": {"Ids": ids}})

    # --- Ключевые фразы (Поиск + контекстный таргетинг РСЯ) ---
    def keywords_add(self, keywords):
        return self.c.call("keywords", "add", {"Keywords": keywords})

    # --- Графические/картиночные ассеты для РСЯ ---
    def adimages_add(self, ad_images):
        """ad_images: [{"Name":..., "ImageData": <base64>}]"""
        return self.c.call("adimages", "add", {"AdImages": ad_images})

    def adimages_get(self, field_names=None):
        return self.c.call("adimages", "get", {
            "SelectionCriteria": {},
            "FieldNames": field_names or ["AdImageHash", "Name", "Type"],
        })

    # --- Аудитории/ретаргетинг (интересы РСЯ, Yandex Audience) ---
    def audiencetargets_add(self, items):
        return self.c.call("audiencetargets", "add", {"AudienceTargets": items})

    def retargetinglists_add(self, lists):
        return self.c.call("retargetinglists", "add", {"RetargetingLists": lists})

    # --- Корректировки ставок (гео/демография/моб/аудитории) ---
    def bidmodifiers_add(self, modifiers):
        return self.c.call("bidmodifiers", "add", {"BidModifiers": modifiers})

    # --- Справочники (регионы гео и т.п.) ---
    def dictionaries_get(self, names):
        return self.c.call("dictionaries", "get", {"DictionaryNames": names})

    def geo_regions(self):
        return self.dictionaries_get(["GeoRegions"])
