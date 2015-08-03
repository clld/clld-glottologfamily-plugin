# clld-glottologfamily-plugin

[clld](https://github.com/clld/clld) plugin, adding language families from 
[Glottolog](http://glottolog.org) to a *clld* app to allow for better navigation and 
visualization.

[![Build Status](https://travis-ci.org/clld/clld-glottologfamily-plugin.svg?branch=master)](https://travis-ci.org/clld/clld-glottologfamily-plugin)
[![codecov.io](http://codecov.io/github/clld/clld-glottologfamily-plugin/coverage.svg?branch=master)](http://codecov.io/github/clld/clld-glottologfamily-plugin?branch=master)

## Usage

To equip a `Language` model with a family relation, the model should inherit from
`clld_glottologfamily_plugin.models.HasFamilyMixin`. This relation can be populated upon
database initialization calling `clld_glottologfamily_plugin.util.load_families`.

The families assigned in this way have an associated icon which can be used as map marker.
To make this easier, a custom `IMapMarker` may inherit from 
`clld_glottologfamily_plugin.util.LanguageByFamilyMapMarker`.

Associated `DataTable` columns suitable for tables listing `Language` objects can be
used as follows:

```python
from clld.web.datatables.language import Languages
from clld_glottologfamily_plugin.datatables import FamilyCol, MacroareaCol
from clld_glottologfamily_plugin.models import Family

from models import CustomLanguage


class LanguagesWithFamily(Languages):
    def base_query(self, query):
        return query.outerjoin(Family)  # note: isolates will have no related family!

    def col_defs(self):
        res = Languages.col_defs(self)
        res.append(MacroareaCol(self, 'macroarea', language_cls=CustomLanguage))
        res.append(FamilyCol(self, 'family', language_cls=CustomLanguage))
        return res
```


### Assigning families

1. Family information is retrieved from Glottolog, based on the `id` attribute of a 
language. This will only work if `id` is either a glottocode or an ISO 639-3 code.

2. If no related family is found, `None` will be assigned - rather than a dummy *isolates*
family or individual one-member families derived from the language.
