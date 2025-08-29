#!/usr/bin/python3
"""
Markdown to HTML
"""

import sys
import os
import re
import hashlib


def convert_markdown(md_content):
    """
    Convert Markdown headings, lists, paragraphs, bold, emphasis,
    and custom syntax to HTML.
    """
    html_content = []
    in_ulist = False
    in_olist = False
    in_paragraph = False
    paragraph_lines = []

    def close_paragraph():
        nonlocal paragraph_lines, in_paragraph
        if paragraph_lines:
            html_content.append('<p>')
            for i, line in enumerate(paragraph_lines):
                if i > 0:
                    html_content.append('<br/>')
                html_content.append(apply_text_styles(line))
            html_content.append('</p>')
            paragraph_lines = []
            in_paragraph = False

    def apply_text_styles(text):
        """ Convert Markdown bold, emphasis, and custom syntax to HTML. """
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.+?)__', r'<em>\1</em>', text)
        text = re.sub(r'\[\[(.+?)\]\]', lambda m: hashlib.md5(
            m.group(1).encode()).hexdigest(), text)
        text = re.sub(r'\(\((.+?)\)\)', lambda m: re.sub(
            r'[cC]', '', m.group(1)), text)
        return text

    for line in md_content.splitlines():
        match_heading = re.match(r'(#{1,6}) (.+)', line)
        if match_heading:
            close_paragraph()
            level = len(match_heading.group(1))
            text = apply_text_styles(match_heading.group(2))
            html_content.append(f'<h{level}>{text}</h{level}>')
            if in_ulist:
                html_content.append('</ul>')
                in_ulist = False
            if in_olist:
                html_content.append('</ol>')
                in_olist = False
        elif line.startswith('- '):
            close_paragraph()
            if in_olist:
                html_content.append('</ol>')
                in_olist = False
            if not in_ulist:
                html_content.append('<ul>')
                in_ulist = True
            html_content.append(f'<li>{apply_text_styles(line[2:])}</li>')
        elif line.startswith('* '):
            close_paragraph()
            if in_ulist:
                html_content.append('</ul>')
                in_ulist = False
            if not in_olist:
                html_content.append('<ol>')
                in_olist = True
            html_content.append(f'<li>{apply_text_styles(line[2:])}</li>')
        else:
            if in_ulist:
                html_content.append('</ul>')
                in_ulist = False
            if in_olist:
                html_content.append('</ol>')
                in_olist = False
            if line.strip():
                paragraph_lines.append(line)
                in_paragraph = True
            else:
                close_paragraph()

    close_paragraph()
    if in_ulist:
        html_content.append('</ul>')
    if in_olist:
        html_content.append('</ol>')

    return '\n'.join(html_content)


def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(md_file):
        sys.stderr.write(f"Missing {md_file}\n")
        exit(1)

    with open(md_file, 'r') as md_filename:
        md_content = md_filename.read()
        html_content = convert_markdown(md_content)

    with open(html_file, 'w') as html_filename:
        html_filename.write(html_content)

    exit(0)


if __name__ == "__main__":
    main()