from krcg import utils
from krcg import vtes
from unidecode import unidecode


SET_MAP = {
    "1996 Promo": "Promo",
    "2003 Tournament promo": "Promo",
    "2004 promo": "Promo",
    "2005 Storyline promo": "Promo",
    "2005 Tournament promo": "Promo",
    "2006 Championship promo": "Promo",
    "2006 EC Tournament promo": "Promo",
    "2006 Storyline promo": "Promo",
    "2006 Tournament promo": "Promo",
    "2007 Promo": "Promo",
    "2008 Storyline promo": "Promo",
    "2008 Tournament promo": "Promo",
    "2009 Tournament / Storyline promo": "Promo",
    "2010 Storyline promo": "Promo",
    "2015 Storyline Rewards": "Promo",
    "2018 Humble Bundle": "Promo",
    "2019 AC Promo": "Promo",
    "2019 ACC Promo": "Promo",
    "2019 DriveThruCards Promo": "Promo",
    "2019 EC Promo": "Promo",
    "2019 Grand Prix Promo": "Promo",
    "2019 NAC Promo": "Promo",
    "2019 Promo": "Promo",
    "2019 Promo Pack 1": "Promo",
    "2019 SAC Promo": "Promo",
    "2020 GP Promo": "Promo",
    "2020 Promo Pack 2": "Promo",
    "2021 Kickstarter Promo": "Promo",
    "2021 Mind’s Eye Theatre Promo": "Promo",
    "2021 Promo Pack 3": "Promo",
    "2021 Resellers Promo": "Promo",
    "2021 SAC Promo": "Promo",
    "2022 European GP Promo": "Promo",
    "Anarch Unbound": "AU",
    "Anarchs": "Anarchs",
    "Anarchs promo": "Promo",
    "Ancient Hearts": "AH",
    "Anthology": "Anthology",
    "Black Hand": "BH",
    "Black Hand promo": "Promo",
    "Blood Shadowed Court": "BSC",
    "Bloodlines": "BL",
    "Bloodlines promo": "Promo",
    "Camarilla Edition": "CE",
    "Camarilla Edition promo": "Promo",
    "Danse Macabre": "DM",
    "Dark Sovereigns": "DS",
    "Ebony Kingdom": "EK",
    "Fall 2002 Storyline promo": "Promo",
    "Fall 2004 Storyline promo": "Promo",
    "Fall of London": "FoL",
    "Fifth Edition": "V5",
    "Fifth Edition (Anarch)": "V5A",
    "Final Nights": "FN",
    "Final Nights promo": "Promo",
    "First Blood": "FB",
    "Gehenna": "Gehenna",
    "Gehenna promo": "Promo",
    "Heirs to the Blood": "HttB",
    "Jyhad": "Jyhad",
    "Keepers of Tradition": "KoT",
    "Kindred Most Wanted": "KMW",
    "Kindred Most Wanted promo": "Promo",
    "Legacies of Blood": "LoB",
    "Legacies of Blood promo": "Promo",
    "Lords of the Night": "LotN",
    "Lost Kindred": "LK",
    "New Blood": "NB",
    "Nights of Reckoning": "NoR",
    "Print on Demand": "POD",
    "Prophecies league promo": "Promo",
    "Sabbat": "Sabbat",
    "Sabbat Preconstructed": "SP",
    "Sabbat War": "SW",
    "Sabbat War promo": "Promo",
    "Summer 2003 Storyline promo": "Promo",
    "Sword of Caine": "SoC",
    "Sword of Caine promo": "Promo",
    "Tenth Anniversary": "Tenth",
    "The Unaligned": "TU",
    "Third Edition": "Third",
    "Third Edition promo": "Promo",
    "Twenty-Fifth Anniversary": "25th",
    "Twilight Rebellion": "TR",
    "V5 Polish Edition promo": "Promo",
    "Vampire: The Eternal Struggle": "VTES",
    "Winter 2002 Storyline promo": "Promo",
}


def pack_line(*args):
    return "\t".join(args) + "\n"


def yield_cards_data():
    vtes.VTES.load_from_vekn()
    yield pack_line(
        "Name",
        "Set",
        "ImageFile",
        "Type",
        "Clan",
        "Group",
        "Capacity",
        "Discipline",
        "PoolCost",
        "BloodCost",
        "Text",
        "Rarity",
    )
    for c in sorted(vtes.VTES, key=lambda c: (c.library, utils.normalize(c._name))):
        filename = c.url.rsplit("/", 1)[1].rsplit(".", 1)[0]
        if c.crypt:
            filename += f",cardbackcrypt"
            disciplines = " ".join(c.disciplines)
        else:
            disciplines = (" & " if c.combo else "/").join(c.disciplines)
        card_text = c.card_text.replace("\t", " ").replace("\n", " ")
        card_text = card_text.replace("/", "").replace("{", "").replace("}", "")
        card_text = card_text.replace("Ⓓ", "(D)")
        yield pack_line(
            unidecode(c.vekn_name),
            SET_MAP[c.ordered_sets[-1]],
            filename,
            "/".join(c.types),
            "/".join(c.clans),
            str(c.group or ""),
            str(c.capacity or ""),
            disciplines,
            str(c.pool_cost or ""),
            str(c.blood_cost or ""),
            unidecode(card_text),
            c._set,
        )


with open("plugin/sets/allsets.txt", "w") as f:
    f.writelines(yield_cards_data())
