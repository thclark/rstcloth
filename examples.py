from rstcloth.rstcloth_builder import RstCloth

__author__ = 'willmcginnis'

if __name__ == '__main__':
    doc = RstCloth(line_width=180)
    doc.title('Example Document')
    doc.newline()
    doc.table(
        ['Column 1', 'Column 2', 'Column 3'],
        data=[
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    )

    doc.print_content()
