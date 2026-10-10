def C(cat, slug, title, desc, inputs, body, about, faqs, extra="", related=None, group=None, eq=None):
    return dict(cat=cat, slug=slug, title=title, desc=desc, inputs=inputs, body=body, about=about, faqs=faqs,
                extra=extra, related=related, group=group, eq=eq)
