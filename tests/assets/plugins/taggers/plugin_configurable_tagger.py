from typing import Optional, Type, Union

from steamship import Tag
from steamship.data import TagValueKey
from steamship.invocable import Config, InvocableResponse, create_handler
from steamship.invocable.plugin_service import PluginRequest
from steamship.plugin.inputs.block_and_tag_plugin_input import BlockAndTagPluginInput
from steamship.plugin.outputs.block_and_tag_plugin_output import BlockAndTagPluginOutput
from steamship.plugin.tagger import Tagger


class TestParserPlugin(Tagger):
    # For testing; mirrors TestConfigurableTagger in Swift

    class TestParserConfig(Config):
        tag_kind: str
        tag_name: str
        number_value: Optional[Union[int, float]] = None
        # TODO: Check to see if python and/or swift removes False from obj.
        # If this is non-optional, the typecheck fails despite the fact that the test passes
        # in a value of false....
        boolean_value: Optional[bool] = False
        string_value: Optional[str] = ""

    config: TestParserConfig

    @classmethod
    def config_cls(cls) -> Type[Config]:
        return cls.TestParserConfig

    def run(
        self, request: PluginRequest[BlockAndTagPluginInput]
    ) -> InvocableResponse[BlockAndTagPluginOutput]:
        tag_kind = self.config.tag_kind
        tag_name = self.config.tag_name
        tag_value = {
            TagValueKey.NUMBER_VALUE: self.config.number_value,
            TagValueKey.BOOL_VALUE: self.config.boolean_value,
            TagValueKey.STRING_VALUE: self.config.string_value,
        }

        if request.data is not None:
            file = request.data.file
            tag = Tag(kind=tag_kind, name=tag_name, value=tag_value)
            if file.tags:
                file.tags.append(tag)
            else:
                file.tags = [tag]
            return InvocableResponse(data=BlockAndTagPluginOutput(file=file))


handler = create_handler(TestParserPlugin)
