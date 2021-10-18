"""
Pandoc filter to create a list of abbreviations that is injected into
the Pandoc AST. Will work for any output format supported by Pandoc.
Users control where the list of abbreviations appears in the document by
placing the following code at their location of choice:
<div id="list-of-abbrs"></div>

Users define abbreviations in their R Markdown/Markdown file by
wrapping the text in square brackets and adding `.abbr` attribute:

Example:
    [World Health Organization (WHO)]{.abbr}

The list of abbreviations will exclude duplicate entries and will
be sorted alphabetically, by default.
"""

import panflute as pf
import re

list_of_abbrs = []

def find_abbreviations(el, doc):
    if isinstance(el, pf.Span):
        if 'abbr' in el.classes:
            as_text = pf.stringify(el)
            abbr = re.search("\(.*\)", as_text).group()
            abbr = re.sub('[()]', '', abbr)
            words = re.sub("\(.*\)", '', as_text)
            words = words[0].capitalize() + words[1:].strip()
            list_of_abbrs.append(f'{abbr} - {words}')

def inject_loa(el, doc):
    if isinstance(el, pf.Div):
        if 'list-of-abbrs' in el.identifier:
            global list_of_abbrs
            list_of_abbrs = sorted(set(list_of_abbrs))
            content = pf.Para(pf.Str('\n\n'.join(list_of_abbrs)))
            return content

def main(doc=None):
    return pf.run_filters([find_abbreviations, inject_loa], doc=doc)

if __name__ == "__main__":
    main()
