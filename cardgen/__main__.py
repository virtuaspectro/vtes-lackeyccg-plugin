from krcg import vtes
from unidecode import unidecode


def _write_card(f, c):
    filename = c.url.rsplit("/", 1)[1].rsplit(".", 1)[0]
    cardname = unidecode(c._name)
    if c.crypt:
        filename += f",cardbackcrypt"
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
    card_text = card_text.replace("/", "").replace("{", "").replace("}", "")
    card_text = card_text.replace("Ⓓ", "(D)")
    f.write(
        "\t".join(
            [
                cardname,
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
            ]
        )
        + "\n"
    )


def main():
    vtes.VTES.load_from_vekn()
    with open("plugin/sets/allsets.txt", "w") as f:
        f.write(
            "Name	Set	ImageFile	Type	Clan	Group	Capacity	Discipline	PoolCost	BloodCost	Text	Rarity\n"
        )
        cards = sorted(
            vtes.VTES, key=lambda c: (c.library, unidecode(c._name).casefold())
        )
        for c in cards:
            _write_card(f, c)


main()
