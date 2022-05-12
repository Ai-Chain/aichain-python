import base64
import dataclasses
import json

__copyright__ = "Steamship"
__license__ = "MIT"

from steamship.base.binary_utils import flexi_create
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput


def test_dump_string():
    data, mime, encoding = flexi_create(string="Hi")
    assert (data == "Hi")


def test_dump_json():
    assert (json.dumps(flexi_create(json="Hi")[0]) == '"Hi"')
    assert (json.dumps(flexi_create(json=True)[0]) == 'true')
    assert (json.dumps(flexi_create(json=1.2)[0]) == '1.2')
    assert (json.dumps(flexi_create(json=[1, 2, 3])[0]) == '[1, 2, 3]')
    assert (json.dumps(flexi_create(json={'hi': 'there'})[0]) == '{"hi": "there"}')

    @dataclasses.dataclass
    class Person:
        name: str

    person = Person(name="Ted")
    assert (json.dumps(flexi_create(json=person)[0]) == '{"name": "Ted"}')

    @dataclasses.dataclass
    class Person2:
        name: str

        def to_dict(self):
            return {"takes": "precedence"}

    person2 = Person2(name="Ted")
    assert (json.dumps(flexi_create(json=person2)[0]) == '{"takes": "precedence"}')


def _base64_decode(base64_message: str) -> str:
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    return message_bytes.decode('utf8')


def test_dump_raw_data():
    """This makes use of flexi_create. We want to ensure it is properly base64 encoding the JSON representation of
    objects given to it."""

    obj = RawDataPluginOutput(json={'hi': 'there'})
    json_str = _base64_decode(obj.data)
    assert(json_str == '{"hi": "there"}')

    @dataclasses.dataclass
    class Person:
        name: str

    person = Person(name="Ted")
    obj2 = RawDataPluginOutput(json=person)
    json_str2 = _base64_decode(obj2.data)
    assert (json_str2 == '{"name": "Ted"}')