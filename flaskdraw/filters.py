from flaskdraw import app

# CUSTOM JINJA2 FILTERS HERE:
@app.template_filter()
def pretty_date(dttm):
    if dttm:
        return dttm.strftime("%Y-%m-%d")
    else:
        return "----------"
