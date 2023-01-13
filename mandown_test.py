import mandown

comic = mandown.query("https://mangadex.org/title/72331318-7f5e-44b3-8510-12133149fde3/isekai-walking")
mandown.download(comic)
mandown.convert(comic, comic.metadata.title, "epub")