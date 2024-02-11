# chrome headless

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

BASE_HEADLESS_CHROME_ARGS = [
    '--headless',
    '--enable-logging',
    '--disable-extensions',
    '--print-to-pdf-no-header',
    '--disable-popup-blocking ',
    '--run-all-compositor-stages-before-draw',
    '--disable-checker-imaging',
    '--virtual-time-budget=10000',
]


def chrome_cmd(url, path):
    """
    Given URL input, and ouput path, get headless chrome command as list
    of args for subprocess.Popen to use
    """
    _path = path.replace(' ', '\ ')
    arg_output = '--print-to-pdf={}'.format(_path)
    return [CHROME] + BASE_HEADLESS_CHROME_ARGS + [
        arg_output,
        url,
    ]


