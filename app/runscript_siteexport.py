from plone import api
from plone import rfc822
from plone.dexterity.utils import iterSchemata
from plone.memoize import ram
from zope.component.hooks import setSite
from zope import schema

import functools
import os
import sys

# global path to where export dirs get put:
OUTPUT_BASE = '/Volumes/general/siteexport'

IGNORE_PATHS = [
    'events/',
]

FOLDERISH_TYPES = [
    'collective.teamwork.project',
    'collective.teamwork.team',
    'collective.teamwork.workspace',
    'Folder',
    'uu.formlibrary.library',
    'uu.formlibrary.series',
    'uu.formlibrary.measurelibrary',
    'uu.chart.report',
]


ALL_CONTENT_QUERY = {
    'path': '/',
}

@ram.cache(lambda v: 1)
def site_id():
    return api.portal.get().getId()


def _get(spec):
    if type(spec) in (type(u''), type('')):
        return api.portal.get().unrestrictedTraverse(spec)
    if spec.__class__.__name__ == 'mybrains':
        return spec._unrestrictedGetObject()


def site_relative_path(path, siteid=None):
    _path = path
    if isinstance(_path, unicode):
        _path = str(path)
    if isinstance(_path, str):
        _path = _path.split('/')
    _path = [part for part in _path if part]  # no empty leading
    if _path[0] == siteid or site_id():
        _path.pop(0)
    return '/'.join(_path)


def pathcmp(a, b):
    n_a = len(str(a).split('/'))
    n_b = len(str(b).split('/'))
    if n_a == n_b:
        return 0
    return -1 if n_a < n_b else 1


def sorted_paths(paths):
    return sorted(paths, key=functools.cmp_to_key(pathcmp))


def all_content_brains():
    catalog = api.portal.get_tool('portal_catalog')
    return catalog.unrestrictedSearchResults(ALL_CONTENT_QUERY)


def _ignore_path(path):
    for _part in IGNORE_PATHS:
        if path.startswith(_part):
            return True
    return False


def depth_sorted_content_paths():
    """
    All paths to site content, sorted by containment depth level
    """
    siteid = site_id()
    _paths = [
        site_relative_path(brain.getPath(), siteid)
        for brain in all_content_brains()
    ]
    return sorted_paths([
        p for p in _paths if not _ignore_path(p)
    ])


def safe_mkdir(path):
    """make dir if it does not already exist"""
    if not os.path.isdir(path):
        if not os.path.exists(path):
            os.mkdir(path)
        else:
            raise('Non-directory exists at base export path')


def _mktargetdir(path):
    """given path relative to site, mkdir for that path if needed in output"""
    site_output_path = os.path.join(OUTPUT_BASE, site_id())
    safe_mkdir(os.path.join(site_output_path, path))


def _bootstrap_export_dir(siteid):
    site_output_path = os.path.join(OUTPUT_BASE, siteid)
    for path in [OUTPUT_BASE, site_output_path]:
        if not os.path.isdir(path):
            if not os.path.exists(path):
                os.mkdir(path)
            else:
                raise('Non-directory exists at base export path')
    return site_output_path


def export_item(content, path):
    pass


def schema_fields(content):
    fields = [
        schema.getFieldsInOrder(_schema) for _schema in iterSchemata(content)
    ]
    return list(dict(itertools.chain(*list(filter(any, fields)))).values())


def folder_path(path):
    site_output_path = os.path.join(OUTPUT_BASE, site_id())
    return os.path.join(site_output_path, path)


def export_folder_metadata(content, path):
    rfc822_msg = rfc822.constructMessageFromSchemata(
        content, iterSchemata(content))
    _text = rfc822.renderMessage(rfc822_msg)
    with open(os.path.join(folder_path(path), 'metadata.txt'), 'w') as f:
        f.write(_text)


def export_folder(content, path):
    _mktargetdir(path)
    export_folder_metadata(content, path)


def _export_site(site):
    output_path = _bootstrap_export_dir(site.getId())
    for path in depth_sorted_content_paths():
        content = _get(path)
        if content.portal_type in FOLDERISH_TYPES:
            export_folder(content, path)
        else:
            export_item(content, path)
    print('Output site to {}'.format(output_path))


def main(app, argv):
    if len(argv) < 4:
        raise RuntimeError('site name argument not provided')
    siteid = argv[3].strip()
    if siteid not in app.objectIds():
        raise ValueError('No site with id {}'.format(siteid))
    site = app[siteid]
    setSite(site)
    _export_site(site)


if __name__ == '__main__' and 'app' in locals():
    main(app, sys.argv)