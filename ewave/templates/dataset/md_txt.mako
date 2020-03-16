${request.dataset.formatted_editors()|n} (eds.) ${request.dataset.published.year}.
${request.dataset.description or request.dataset.name}. Zenodo.
DOI: ${request.dataset.jsondata['doi']}
(Available online at http://${request.dataset.domain}, Accessed on ${h.datetime.date.today()}.)
