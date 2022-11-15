from krcg import cards
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

PRECONS_MAP = {
    k: {w: u for u, w in v.items()} for k, v in cards.Card._RARITY_PRECON_CODES.items()
}
PRECONS_MAP["Promo"] = {"Humble Bundle": "HB"}
CLANS_MAPS = {
    "Banu Haqim": "Assamite",
    "Ministry": "Follower of Set",
}


def _write_card(f, c):
    filename = c.url.rsplit("/", 1)[1].rsplit(".", 1)[0]
    setname = SET_MAP[c.ordered_sets[0]]
    cardname = unidecode(c._name)
    if c.crypt:
        # TODO add "any" suffix for consistency
        if filename[-3:] == "any":
            filename = filename[:-3]
        filename += f",cardbackcrypt"
        setname += "M"
        disciplines = " ".join(c.disciplines)
        suffixes = []
        if c.is_evolution:
            suffixes.append(f"G{c.group}")
        if c.adv:
            suffixes.append("ADV")
        if suffixes:
            cardname += f" ({' '.join(suffixes)})"
    else:
        if c.combo:
            separator = " & "
        else:
            separator = "/"
        disciplines = separator.join(c.disciplines)
    card_text = c.card_text.replace("\t", " ").replace("\n", " ")
    card_text = card_text.replace("Ⓓ", "(D)")
    card_text = card_text.replace("Blood Sorcery", "Thaumaturgy")
    card_text = card_text.replace("Banu Haqim", "Assamite")
    card_text = card_text.replace("Ministry", "Follower of Set")
    card_text = card_text.replace("/", "").replace("{", "").replace("}", "")
    f.write(
        "\t".join(
            [
                cardname,
                # TODO: replace by last set, use real name
                setname,
                filename,
                SET_MAP[c.ordered_sets[-1]],
                "/".join(c.types),
                "/".join(CLANS_MAPS.get(clan, clan) for clan in c.clans),
                str(c.group or ""),
                str(c.capacity or ""),
                # TODO: Thaumaturgy -> Blood Sorcery?
                disciplines,
                # TODO: indicate costs
                "",  # str(c.pool_cost or ""),
                "",  # str(c.blood_cost or ""),
                unidecode(card_text),
                _generate_set(c._set),
                "; ".join(unidecode(a) for a in c.artists),
            ]
        )
        + "\n"
    )


def _generate_set(sets):
    ret = []
    has_promo = False
    for s in sets.split(","):
        s = s.strip()
        if s.startswith("Promo-"):
            if has_promo:
                continue
            else:
                s = "Promo"
                has_promo = True
        ret.append(s)
    return ", ".join(ret)


def main():
    vtes.VTES.load_from_vekn()
    with open("plugin/sets/allsets.txt", "w") as f:
        f.write(
            "Name	SET	ImageFile	Expansion	Type	Clan	Group	Capacity	Discipline	PoolCost	BloodCost	Text	Rarity	Artist\n"
        )
        cards = sorted(
            vtes.VTES, key=lambda c: (c.library, unidecode(c._name).casefold())
        )
        for c in cards:
            _write_card(f, c)


main()
