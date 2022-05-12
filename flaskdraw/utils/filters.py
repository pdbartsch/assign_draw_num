from flask import Blueprint

utils = Blueprint("utils", __name__)

# Custom Filters
@utils.template_filter("my_multiplier")
def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)


# CUSTOM JINJA2 FILTERS HERE:
@utils.template_filter()
def pretty_date(dttm):
    if dttm:
        return dttm.strftime("%Y-%m-%d")
    else:
        return "----------"


@utils.template_filter()
def date_to_year(dttm):
    if dttm:
        return dttm.strftime("%Y")
    else:
        return "----"
