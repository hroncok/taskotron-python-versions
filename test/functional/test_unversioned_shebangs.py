import os
import pytest

from taskotron_python_versions.unversioned_shebangs import (
    matches,
    get_problematic_files,
    get_scripts_summary,
)
from taskotron_python_versions.common import Package

fixtures_dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))) + '/fixtures/'


@pytest.mark.parametrize(('line', 'query', 'expected'), (
    (b'#!/usr/bin/python', b'#!/usr/bin/python', True),
    (b'#!/usr/bin/python ', b'#!/usr/bin/python', True),
    (b'#!/usr/bin/python -I', b'#!/usr/bin/python', True),
    (b'#!/usr/bin/python #comment', b'#!/usr/bin/python', True),
    (b'#!/usr/bin/python3', b'#!/usr/bin/python', False),
    (b'#!/usr/bin/python2', b'#!/usr/bin/python', False),
    (b'#!/usr/bin/env python', b'#!/usr/bin/env python', True),
    (b'#!/usr/bin/env python -I', b'#!/usr/bin/env python', True),
    (b'#!/usr/bin/env python3', b'#!/usr/bin/env python', False),
    (b'#!/usr/bin/env python2', b'#!/usr/bin/env python', False),
    (b'#!/usr/bin/env perl', b'#!/usr/bin/env python', False),
))
def test_matches(line, query, expected):
    assert matches(line, query) == expected


@pytest.mark.parametrize(('archive', 'query', 'expected'), (
    ('tracer-0.6.9-2.fc25.noarch.rpm',
     '#!/usr/bin/python', {'/usr/bin/tracer'}),
    ('python3-django-1.10.7-1.fc26.noarch.rpm', '#!/usr/bin/env python',
     {'/usr/lib/python3.6/site-packages/django/bin/django-admin.py',
      ('/usr/lib/python3.6/site-packages/'
       'django/conf/project_template/manage.py-tpl')}),
    ('python3-django-1.10.7-1.fc26.noarch.rpm', '#!/usr/bin/python', set()),
    ('pyserial-2.7-6.fc25.noarch.rpm', '#!/usr/bin/python', set()),
))
def test_get_problematic_files(archive, query, expected):
    assert get_problematic_files(fixtures_dir + archive, query) == expected


@pytest.mark.parametrize(('path', 'expected'), (
    ('tracer-0.6.9-2.fc25.noarch.rpm',
     {'#!/usr/bin/python': {'/usr/bin/tracer'},
      '#!/usr/bin/env python': set()}),
    ('python3-django-1.10.7-1.fc26.noarch.rpm',
     {'#!/usr/bin/python': set(),
      '#!/usr/bin/env python':
      {'/usr/lib/python3.6/site-packages/django/bin/django-admin.py',
       ('/usr/lib/python3.6/site-packages/'
        'django/conf/project_template/manage.py-tpl')}}),
    ('pyserial-2.7-6.fc25.noarch.rpm',
     {'#!/usr/bin/python': set(),
      '#!/usr/bin/env python': set()}),
))
def test_get_scripts_summary(path, expected):
    package = Package(fixtures_dir + path)
    assert get_scripts_summary(package) == expected
