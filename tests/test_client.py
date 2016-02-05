import pytest
from mock import Mock, patch

from yom.cli import Yom
from yom.errors import *


@patch.object(Yom, 'prepare_view')
@patch.object(Yom, 'init_crawler')
def test_controller(init_crawler_mock, prepare_view_mock):
    init_crawler_mock.return_value = None
    prepare_view_mock.return_value = lambda **kw: {
        'header': 'ok', 'table': [['param1', 'value1'], ['param2', 'value2']]}

    args = Mock()
    args.action = 'edit'
    args.app_hash = '1' * 32
    args.input_title = 'test app'
    args.input_scopes = ['login:avatar']

    context = Yom(args)._run()
    assert 'header' in context
    assert 'table' in context
    assert context['header'] in 'ok'


def test_validation():
    args = Mock()
    args.action = 'edit'
    args.input_title = 'test app'
    args.input_scopes = ['login:avatar']

    yom = Yom(args)

    with pytest.raises(YomValidationError):
        yom._run()

    with pytest.raises(YomValidationError):
        yom.args.title = None
        Yom(args)._run()
