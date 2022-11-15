from krcg import utils
from krcg import vtes
from unidecode import unidecode


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
            c.ordered_sets[-1],
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
