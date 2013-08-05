from lxml import html
from lxml.etree import XPathEvalError, ParserError

from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext


class XPathForm(forms.Form):
    q = forms.CharField()
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': '20'}))


def run_xpath(request):
    """Take a form and return the nodes selected"""
    if request.method == 'POST':
        form = XPathForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            text = cd['text']
            q = cd['q']

            # Make a good HTML tree
            try:
                html_tree = html.fromstring(text)
            except ParserError, e:
                return render_to_response(
                    'index.html',
                    {'form': form,
                     'lazy_error': 'Unable to parse document: %s' % e},
                    RequestContext(request)
                )

            def remove_anchors(href):
                # We don't like anchors. Away they go.
                return href.split('#')[0]
            html_tree.rewrite_links(remove_anchors)

            # Run the xpath, and return the results
            try:
                nodes = html_tree.xpath(q)
            except XPathEvalError, e:
                return render_to_response('index.html',
                                          {'form': form,
                                           'lazy_error': 'Invalid XPath Expression: %s' % e},
                                          RequestContext(request))
            if type(nodes) == bool:
                return render_to_response('index.html',
                                          {'form': form,
                                           'lazy_warning': 'Your query did not return any elements, but instead '
                                                           'returned the boolean: \'%s\'' % nodes},
                                          RequestContext(request))
            else:
                node_strings = []
                for node in nodes:
                    try:
                        s = html.tostring(node,
                                          encoding='unicode',
                                          pretty_print=True).strip()
                        node_strings.append(s)
                    except TypeError:
                        # Returned a text node, not an element.
                        if len(node.strip()) > 0:
                            node_strings.append(node)

            return render_to_response('index.html',
                                      {'form': form,
                                       'node_strings': node_strings},
                                      RequestContext(request))

    else:
        # Form is loading for the first time
        form = XPathForm()

    return render_to_response('index.html',
                              {'form': form},
                              RequestContext(request))
