"""
Converts label in a textgrid file to ARPABET format.

Usage:
    replace.py --input-textgrid=<it> --output-textgrid=<ot>

Options:
    --input-textgrid=<it>        Input textgrid
    --output-textgrid=<o>        Output textgrid
"""

from docopt import docopt
import tgt

if __name__ == "__main__":

    args = docopt(__doc__)
    input_textgrid = args["--input-textgrid"]
    output_textgrid = args["--output-textgrid"]

    with open("data/phone_map") as f:
        phone_data = f.readlines()

        phone_map = {item.split()[0]: item.split()[1] for item in phone_data}
        sorted_phone_map = {
            k: v
            for k, v in sorted(
                phone_map.items(), key=lambda item: item[0], reverse=True
            )
        }

    tg = tgt.read_textgrid(input_textgrid)
    tier_names = tg.get_tier_names()
    for tier in tier_names:
        tier_obj = tg.get_tier_by_name(tier)
        for idx, item in enumerate(tier_obj):
            label = item.text
            label = label.replace(label, phone_map[label])
            tier_obj[idx].text = label

    tgt.io.write_to_file(tg, output_textgrid, format="long")
