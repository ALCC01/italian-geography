# Italian geography 🇮🇹🇪🇺

Flashcard deck for [Anki][anki] on 🇮🇹 Italian political geography for those who
didn't pay attention in primary school, or those who wish to learn about Italy.

## ✨ Features

This deck includes:
* 127 unique notes about Italy's Regions, Autonomous Provinces, Metropolitan
Cities and Provinces
* 134 maps
* 155 tags

> 🗣 **Language**: The deck is currently available in **Italian**, although this
should not be a barrier to anyone unfamiliar with the language.

## 🚀 Getting started

If you're new to Anki, start with [this guide][anki-getting-started].

1. [Download the latest release of the deck here][itgeo-release]
2. Open Anki and go to `File > Import`
3. Select the .apkg file you downloaded
4. In the import dialog, click `Import`
5. The deck will appear in your collection

## 🔄 Upgrading

> [!WARNING] 
> ⚠ Upgrading the deck will overwrite your existing notes, and you will lose any
> edits you may have made (but you will keep your review history and
> scheduling). Unfortunately, there is currently no easy workaround to preserve
> custom changes during the upgrade process.

To upgrade:

* Follow the same steps as in the “Getting Started” section
* In the import dialog, ensure that Update existing notes is set to `Always` or
`If newer`

## 🗂️ Deck structure

### 📝 Cards

The notes use a custom note type called `Geographical Entity` and cards are
generated from six templates. You can suspend individual cards based on their
template if you prefer not to study certain formats.

* `Label - Map` and `Map - Label` – Connect each geographical entity to its
location within Italy
* `Label - Capital` and `Capital - Label` – Link each Region to its capital city
(_capoluogo_). These cards are used sparingly for Provinces, since most are
already named after their capital(s)
* `Label - Abbreviation` and `Abbreviation - Label` – Pair each Province with
its official two-letter abbreviation (_sigla automobilistica_)

<table>
  <tr><th scope="col">Front</th><th scope="col">Back</th></tr>
  <tr><th scope="col" colspan="2">Label - Map</th></tr>
  <tr>
    <td><img src="doc/Label - Map -- Front.png"></td>
    <td><img src="doc/Label - Map -- Back.png"></td>
  </tr>
  <tr><th scope="col" colspan="2">Map - Label</th></tr>
  <tr>
    <td><img src="doc/Map - Label -- Front.png"></td>
    <td><img src="doc/Map - Label -- Back.png"></td>
  </tr>
  <tr><th scope="col" colspan="2">Label - Capital</th></tr>
  <tr>
    <td><img src="doc/Label - Capital -- Front.png"></td>
    <td><img src="doc/Label - Capital -- Back.png"></td>
  </tr>
  <tr><th scope="col" colspan="2">Capital - Label</th></tr>
  <tr>
    <td><img src="doc/Capital - Label -- Front.png"></td>
    <td><img src="doc/Capital - Label -- Back.png"></td>
  </tr>
  <tr><th scope="col" colspan="2">Label - Abbreviation</th></tr>
  <tr>
    <td><img src="doc/Label - Abbreviation -- Front.png"></td>
    <td><img src="doc/Label - Abbreviation -- Back.png"></td>
  </tr>
  <tr><th scope="col" colspan="2">Abbreviation - Label</th></tr>
  <tr>
    <td><img src="doc/Abbreviation - Label -- Front.png"></td>
    <td><img src="doc/Abbreviation - Label -- Back.png"></td>
  </tr>

</table>

### 🏷️ Tags

The deck provides 155 tags to help you with filtering. They are especially
useful when creating filtered decks or suspending notes you don’t wish to study.
Tags are structured into the following categories:

* `itgeo::area` – Filters notes by Italy’s five major statistical areas:
North-East, North-West, Center, South, and Isles
* `itgeo::regione` – Filters notes by Italy’s 20 Regions
* `itgeo::tipo` – Categorizes notes by the type of entity described (e.g.,
Region or Province)
* `itgeo::suspend` – Marks notes that are obvious or redundant, and can be
safely suspended during study
* `itgeo::NUTS` – Assigns each note its corresponding NUTS 2024 code

## 🟡 Caveats

* In some Regions, **Provinces have been formally abolished** or replaced by
bodies with different names, though these new entities largely retain the same
functions and territorial boundaries. However, since Provinces are still widely
used for statistical and postal purposes, and most people continue to refer to
them as "Provinces," this deck maintains that terminology for clarity and
consistency.
* **Trentino-Alto Adige/Südtirol** is not included, as most people identify the
Region by its two Autonomous Provinces, Trento and Bolzano/Bozen, which also
carry out most of the regional-level functions
* **Sardinia**'s provincial boundaries are undergoing administrative changes.
The current version of the deck reflects the previous structure as represented
by NUTS 2024, which does not align with the most recent reorganization

## 👷 Contributing

Contributions are welcome! Just open an issue or a pull request if you think you
can contribute something cool to the deck.

### Building

To build the project, you will need to create a venv and install the
dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 generate.py
```

To build the README.md, build the deck and then run
`python3 utiles/gen_readme.py > README.md` (it will use data from the build to
update values in the text).

### Project structure

The project revolves around using a Python script to transform CSV data into
Anki notes in a reliable and reproducible manner. The project folder is
structured as follows:

- `generate.py` is the main script that will ingest data and output the .apkg
file in the `build/` directory
- `data/`
  - `entities.csv` is the main source of knowledge used to generate notes
  - `gis/` contains a QGIS project used to generate the maps
- `media/` holds all media used by the deck (ie maps)
- `templates/` holds the templates used by the cards
  - `style.css` is a commond stylesheet used by all cards
  - `README.md.template` is used as a template to generate the main README.md
  file
- `utils/` contains utility script for the project (such as `gen_readme.py`)
- `build/` is where the build artifacts will be stored
  - `itgeo.apkg` is the finished product
  - `buildinfo.json` is used by `gen_readme.py` to update values in the text

## 🙏 Acknowledgments

* Card templates are based on [Ultimate Geography][ug], released under the
Unlicense
* NUTS boundaries used to render the maps are provided by
[Eurostat][nuts-license], © EuroGeographics
* Administrative data sourced from [ISTAT][istat-data]

## 📄 License

Copyright © 2025 Alberto Coscia. Released under the [CC BY 4.0][license]
license. Made in 🇪🇺 Italy, Europe.

[anki]: http://ankisrs.net/
[anki-getting-started]: https://docs.ankiweb.net/getting-started.html
[itgeo-release]: https://github.com/ALCC01/italian-geography/releases/latest
[ug]: https://github.com/anki-geo/ultimate-geography
[nuts-license]: https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units
[istat-data]: https://www.istat.it/classificazione/codici-dei-comuni-delle-province-e-delle-regioni/
[license]: https://creativecommons.org/licenses/by/4.0/

