import os
import nose
from nose.tools import raises
import mercy.models
import mercy.importers.fda
import mercy.exceptions

VALID_ROWS=[]

FIXTUREFILE=os.path.abspath(
    os.path.join(
        __file__,
        "..",
        "fixtures",
        "fda_database.tar.gz"
        )
    )

FIXTUREFILE_BAD=os.path.abspath(
    os.path.join(
        __file__,
        "..",
        "fixtures",
        "fda_database_bad.tar.gz"
        )
    )

FIXTUREFILE_CORRUPT=os.path.abspath(
    os.path.join(
        __file__,
        "..",
        "fixtures",
        "fda_database_corrupt.tar.gz"
        )
    )

@raises(mercy.exceptions.CorruptTarError)
def test_fda_import_fails_on_corrupt_tar():
    importer = mercy.importers.fda.FDAImporter()
    impoter.read(FIXTUREFILE_CORRUPT)

def test_fda_import_populates_table():
    importer = FDAImporter().read(FIXTUREFILE)
    rows = mercy.models.fda.Product.query.all()
    for i in range(0, len(rows)):
        row = rows[i]
        canned_row = CANNED_ROWS[i]
        assert(len(row) == len(canned_row))
        for j in canned_row.keys():
            assert(row[j] == canned_row[j])

@raises(AttributeError, KeyError, ValueError)
def test_fda_import_rejects_bad_records:
    importer = mercy.importers.fda.FDAImporter()
    importer.read(FIXTUREFILE_BAD)

