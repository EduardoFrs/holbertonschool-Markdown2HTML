#!/usr/bin/python3
"""
Markdown to HTML
"""
import sys
import os

def main():
    # Check if correct number of arguments is provided
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    # Get input and output file names from command line arguments
    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if markdown file exists
    if not os.path.exists(markdown_file):
        sys.stderr.write(f"Missing {markdown_file}\n")
        sys.exit(1)

    # If all checks pass, exit successfully
    sys.exit(0)

if __name__ == "__main__":
    main()
