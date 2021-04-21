import yaml
from textwrap import dedent
import pathlib

def tag_in_item(item, tag_str):
    if tag_str is None:
        return True
    all_tags = []
    for k, e in item['tags'].items():
        all_tags.extend(e)
    return tag_str in all_tags


def generate_tag_set(all_items):

    tag_set = set()
    for item in all_items:
        for k, e in item['tags'].items():
            for t in e:
                tag_set.add(t)
    return tag_set


def build_from_items(items, filename, display_name):

    # Build the gallery file
    panels_body = []
    for item in items:
        if not item.get('thumbnail'):
            item['thumbnail'] = '../_static/images/ebp-logo.png'

        tag_set = set()
        for k, e in item['tags'].items()
                for t in e:
                    tag_set.add(t)

        tags = [f'{{badge}}`{tag},badge-primary badge-pill`' for tag in tag_Set]
        tags = '\n'.join(tags)

        authors = [a.get("name", "anonymous") for a in item['authors']]

        if len(authors) == 1:
            authors_str = f'Created by: {authors[0]}'
        elif len(authors) == 2:
            authors_str = f'Created by: {authors[0]} and {authors[1]}'

        email = [a.get("email", None) for a in item['authors']][0]
        email_str = '' if email == None else f'Email: {email}'

        affiliation = [a.get("affiliation", None) for a in item['authors']][0]
        affiliation_str = '' if affiliation == None else f'Affiliation: {affiliation}'

        affiliation_url = [a.get("affiliation_url", None) for a in item['authors']][0]
        affiliation_url_str = '' if affiliation_url == None else f'{affiliation} Site: {affiliation_url}'

        panels_body.append(
            f"""\
---
:img-top: {item["thumbnail"]}
+++
**{item["title"]}**

{authors_str}

{email_str}

{affiliation_str}

{affiliation_url_str}
 
```{{dropdown}} {item['description'][0:100]} ... <br> **See Full Description:**
{item['description']}
```

```{{link-button}} {item["url"]}
:type: url
:text: Visit Website
:classes: btn-outline-primary btn-block
```

{tags}
"""
        )
    panels_body = '\n'.join(panels_body)

    panels = f"""
# {display_name} Gallery

<div>
  <button class="btn btn-sm btn-primary" data-toggle="collapse" data-target="#packages">Packages</button>
  <div id="packages" class="collapse">
    <a href="#">Pure Python</a>
    <a href="#">Numpy</a>
    <a href="#">Jupyter</a>
  </div>
</div>


````{{panels}}
:container: full-width
:column: text-left col-6 col-lg-4
:card: +my-2
:img-top-cls: w-75 m-auto p-2
:body: d-none
{dedent(panels_body)}
````
"""

    pathlib.Path(f'pages/{filename}.md').write_text(panels)



def main(app):

    with open('links.yaml') as fid:
        all_items = yaml.safe_load(fid)

    build_from_items(all_items, 'links', 'External Links')

    tag_set = generate_tag_set(all_items)
    

    for tag in tag_set:

        items=[]
        for item in all_items:
            if tag_in_item(item, tag):
                items.append(item)

        build_from_items(items, 'links/{tag}', 'External Links - "{tag}"')
        
        



def setup(app):
    app.connect('builder-inited', main)