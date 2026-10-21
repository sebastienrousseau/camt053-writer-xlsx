# SPDX-FileCopyrightText: 2026 Sebastien Rousseau <sebastian.rousseau@gmail.com>
# SPDX-License-Identifier: Apache-2.0 OR MIT
#
# Rendered with `make demo` (VHS, https://github.com/charmbracelet/vhs)
# from a virtual environment where the package is installed. Runs the
# repository's own examples against the statements they ship; no network.

Output .github/demo.gif

Set Shell "bash"
Set FontSize 15
Set Width 1200
Set Height 640
Set Padding 20
Set Theme "Catppuccin Mocha"
Set TypingSpeed 35ms

# The examples write their workbooks to the current directory, so they
# run from a scratch copy rather than the checkout.
Hide
Type "export PS1='$ ' && rm -rf /tmp/xlsx-demo && mkdir /tmp/xlsx-demo && cp -R examples /tmp/xlsx-demo/ && cd /tmp/xlsx-demo && clear"
Enter
Show

Type "python examples/01_minimal_write.py"
Enter
Wait /\$$/
Sleep 2s

Type `python -c "from openpyxl import load_workbook as L; [print(f'{ws.title:9}', ws.max_row - 1, 'row(s)') for ws in L('out_minimal.xlsx')]"`
Enter
Wait /\$$/
Sleep 3s

Type "python examples/02_filter_reversals.py"
Enter
Wait /\$$/
Sleep 4s

Hide
Type "cd - >/dev/null && rm -rf /tmp/xlsx-demo"
Enter
