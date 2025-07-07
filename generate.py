#!/usr/bin/env python3

import genanki
import os
import pandas as pd
import re
import unicodedata
import logging
import json

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO").upper(),
    format="%(levelname)s - %(message)s",
)

CWD_DIR = os.path.abspath(os.path.dirname(__file__))
MEDIA_DIR = os.path.join(CWD_DIR, "media")
DATA_DIR = os.path.join(CWD_DIR, "data")
BUILD_DIR = os.path.join(CWD_DIR, "build")
TEMPLATE_DIR = os.path.join(CWD_DIR, "templates")
DECK_ID = 1753847914  # Hardcoded deck ID
ENTITY_MODEL_ID = 1666296128  # Harcoded note model ID

logging.debug(f"Using CWD {CWD_DIR}")


def load_templates():
    """Loads HTML card templates from templates/"""
    templates = {}
    for filename in os.listdir(TEMPLATE_DIR):
        if not filename.endswith(".html"):
            continue

        with open(os.path.join(TEMPLATE_DIR, filename), "r") as file:
            raw = file.read()
            front, _, back = raw.partition("\n--\n")

        templates[filename.removesuffix(".html")] = (front, back)
    return templates


def load_style():
    """Loads the card templates stylesheet from templates/styles.css"""
    styles = ""
    with open(os.path.join(TEMPLATE_DIR, "style.css"), "r") as file:
        styles = file.read()
    return styles


def nuts_level_to_type_tag(level):
    """Converts a NUTS level to its corresponding Anki tag"""
    if level == 2:
        return "itgeo::tipo::regione"
    elif level == 3:
        return "itgeo::tipo::provincia"
    else:
        return "itgeo::suspend"  # Countries and groups of regions


def create_slug(text):
    """Converts an entity's label to a slug that can be used in an Anki tag"""
    # Normalize unicode characters (handles accents, etc.)
    text = unicodedata.normalize("NFKD", text)

    # Convert to ASCII, ignoring non-ASCII characters
    text = text.encode("ascii", "ignore").decode("ascii")

    text = text.lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9-]", "", text)

    # Remove multiple consecutive hyphens
    text = re.sub(r"-+", "-", text)

    # Remove leading/trailing hyphens
    return text.strip("-")


def nuts_parent_to_tag(entities, level, nuts):
    """Returns tags based on an entity's parent entities' NUTS codes"""
    # Special case for Trentino-Alto Adige, which is not a NUTS2 region but is
    # represented by two NUTS2 regions (ITH1 and ITH2)
    if nuts == "ITH1" or nuts == "ITH2":
        return "itgeo::regione::trentino-alto-adige"

    level_slug = "area" if level == 1 else "regione" if level == 2 else "provincia"

    row = entities[
        (entities["NUTS Level"] == level) & (entities[f"NUTS{level}"] == nuts)
    ]
    label = row["Label"].values[0]
    slug = create_slug(label)

    return f"itgeo::{level_slug}::{slug}"


def template(name):
    """Returns a template config based on its name"""
    return {
        "name": name,
        "qfmt": templates[name][0],
        "afmt": templates[name][1],
    }


def count_tags(deck):
    """Counts unique tags in the deck"""
    tags = set()
    for note in deck.notes:
        for tag in note.tags:
            if tag != "":
                tags.add(tag)

    return len(tags)


if __name__ == "__main__":
    buildinfo = {}  # Will store numbers about the deck being generated

    templates = load_templates()
    logging.info(f"Loaded {len(templates)} templates.")

    style = load_style()
    logging.info("Loaded style.css")

    entities = pd.read_csv(
        os.path.join(DATA_DIR, "entities.csv"), keep_default_na=False
    )
    logging.info(f"Loaded {len(entities)} entities.")
    buildinfo["entities"] = len(entities)
    buildinfo["nuts2"] = len(entities[entities["NUTS Level"] == 2])
    buildinfo["nuts3"] = len(entities[entities["NUTS Level"] == 3])

    deck = genanki.Deck(DECK_ID, "Geografia d'Italia")

    # Define the Anki note model for political/administrative entities
    entity_model = genanki.Model(
        ENTITY_MODEL_ID,
        "Geographical Entity",
        fields=[
            {"name": "Label"},
            {"name": "Type"},
            {"name": "Capital"},
            {"name": "Abbreviation"},
            {"name": "Map"},
        ],
        css=style,
        sort_field_index=0,
        templates=[
            template("Label - Map"),
            template("Map - Label"),
            template("Abbreviation - Label"),
            template("Label - Abbreviation"),
            template("Label - Capital"),
            template("Capital - Label"),
        ],
    )

    # Generates an Anki note for each entity
    for _, row in entities.iterrows():
        # Skip NUTS level 1 (groups of regions)
        if int(row["NUTS Level"]) == 1:
            continue

        # Skip suppressed provinces in Sardinia
        if row["Type"] == "Provincia soppressa":
            continue

        # This entity's NUTS code
        nuts = row["NUTS3"] or row["NUTS2"] or row["NUTS1"]
        logging.debug(f'Adding {row["Label"]} ({row["Type"]}, {nuts})')

        note = genanki.Note(
            model=entity_model,
            fields=[
                row["Label"],
                row["Type"],
                row["Capital"],
                row["Abbreviation"],
                f'<img src="{nuts}.png">',
            ],
            guid=genanki.guid_for(nuts),
            tags=[
                "itgeo::NUTS::" + str(nuts),
                nuts_level_to_type_tag(int(row["NUTS Level"])),
                (
                    nuts_parent_to_tag(entities, 2, row["NUTS2"])
                    if row["NUTS Level"] >= 3
                    else ""
                ),
                (
                    nuts_parent_to_tag(entities, 1, row["NUTS1"])
                    if row["NUTS Level"] >= 2
                    else ""
                ),
            ],
        )

        deck.add_note(note)

    logging.info(f"Created {len(deck.notes)} notes.")
    buildinfo["notes"] = len(deck.notes)
    buildinfo["tags"] = count_tags(deck)

    # Add media files to the deck
    media_files = [
        os.path.join(MEDIA_DIR, f)
        for f in os.listdir(MEDIA_DIR)
        if os.path.isfile(os.path.join(MEDIA_DIR, f))
    ]
    package = genanki.Package(deck, media_files=media_files)
    logging.info(f"Added {len(media_files)} media files.")
    buildinfo["media"] = len(media_files)

    # Write package and build info to disk
    package.write_to_file(os.path.join(BUILD_DIR, "itgeo.apkg"))
    json.dump(buildinfo, open(os.path.join(BUILD_DIR, "buildinfo.json"), "w"))
    logging.info(f"Wrote package to {os.path.join(BUILD_DIR, 'itgeo.apkg')}")
