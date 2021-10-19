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
list_of_words = []

def find_abbreviations(el, doc):
    if isinstance(el, pf.Span) and 'abbr' in el.classes:
        as_text = pf.stringify(el)
        abbr = re.search("\(.*\)", as_text).group()
        abbr = re.sub('[()]', '', abbr)
        words = re.sub("\(.*\)", '', as_text)
        words = words[0].capitalize() + words[1:].strip()
        list_of_abbrs.append(abbr)
        list_of_words.append(words)

def format_list(loa, low):
    indices = [loa.index(x) for x in sorted(set(loa))]
    loa = [loa[i] for i in indices]
    low = [low[i] for i in indices]
    full_list = []
    for a, w in zip(loa, low):
        full_list.append(pf.Para(pf.Strong(pf.Str(a)), pf.Space, pf.Str(w)))
    return pf.Div(*full_list)

def inject_loa(el, doc):
    if isinstance(el, pf.Div) and 'list-of-abbrs' in el.identifier:
        global list_of_abbrs
        global list_of_abbrs
        content = format_list(list_of_abbrs, list_of_words)
        return content

def main(doc=None):
    return pf.run_filters([find_abbreviations, inject_loa], doc=doc)

if __name__ == "__main__":
    main()
