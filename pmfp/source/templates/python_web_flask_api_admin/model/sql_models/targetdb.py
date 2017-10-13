import re
import inflect
from functools import partial
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.automap import generate_relationship
from sqlalchemy import MetaData


def _camelize_classname(target_project, base, tablename, table):
    "Produce a 'camelized' class name, e.g. "
    "'words_and_underscores' -> 'WordsAndUnderscores'"

    return str(target_project+"_" + tablename[0].upper() +
               re.sub(r'_([a-z])', lambda m: m.group(1).upper(), tablename[1:]))


_pluralizer = inflect.engine()


def pluralize_collection(base, local_cls, referred_cls, constraint):
    "Produce an 'uncamelized', 'pluralized' class name, e.g. "
    "'SomeTerm' -> 'some_terms'"

    referred_name = referred_cls.__name__
    uncamelized = re.sub(r'[A-Z]',
                         lambda m: "_%s" % m.group(0).lower(),
                         referred_name)[1:]
    pluralized = _pluralizer.plural(uncamelized)
    return pluralized


def reflect_db(app, db):
    metadata = MetaData()
    engine = db.get_engine()
    if app.config["MANAGE_TABLES"] is None:
        metadata.reflect(engine)
    else:
        try:
            table_name = list(app.config["MANAGE_TABLES"])
        except:
            table_name = list([app.config["MANAGE_TABLES"]])
        metadata.reflect(engine, only=table_name)
    Base = automap_base(metadata=metadata)
    camelize_classname = partial(
        _camelize_classname, app.config["MANAGE_PROJECT"])
    Base.prepare(engine, reflect=True,
                 classname_for_table=camelize_classname,
                 name_for_collection_relationship=pluralize_collection,
                 generate_relationship=generate_relationship)
    return Base.classes
