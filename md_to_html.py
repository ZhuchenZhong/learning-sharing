import os
from functools import partial

from rich.progress import track as rich_track



print_withNoEnd = partial(print, end='\r')

markdown_files = []
for root, _, files in rich_track(\
    os.walk(os.sep.join(__file__.split(os.sep)[:-1])),
    description='Finding Markdown files'):
    markdown_files.extend(\
        [os.path.join(root, file) for file in files if file.endswith('.md')])


for file in rich_track(markdown_files, description='Writing'):
    with open(file, 'w+', encoding='utf-8') as fp:
        raw = fp.read()
        raw.replace('.md', '.html')
        fp.seek(0)
        fp.write(raw)

