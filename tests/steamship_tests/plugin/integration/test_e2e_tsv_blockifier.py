from steamship_tests import PLUGINS_PATH
from steamship_tests.utils.deployables import deploy_plugin
from steamship_tests.utils.file import upload_file
from steamship_tests.utils.fixtures import get_steamship_client


def test_e2e_tsv_blockifier_plugin():
    csv_blockifier_plugin_path = PLUGINS_PATH / "blockifiers" / "tsv_blockifier.py"
    client = get_steamship_client()

    version_config_template = {
        "text_column": {"type": "string"},
        "tag_columns": {"type": "string"},
        "tag_kind": {"type": "string"},
    }
    instance_config = {"text_column": "Message", "tag_columns": "Category", "tag_kind": "Intent"}

    with deploy_plugin(
        client,
        csv_blockifier_plugin_path,
        "blockifier",
        version_config_template=version_config_template,
        instance_config=instance_config,
    ) as (plugin, version, instance):
        with upload_file(client, "utterances.tsv") as file:
            assert len(file.refresh().blocks) == 0
            file.blockify(plugin_instance=instance.handle).wait()
            # Check the number of blocks
            blocks = file.refresh().blocks
            assert len(blocks) == 5
            # Check if the tags are correctly added
            for block in blocks:
                assert block.tags is not None
                assert len(block.tags) > 0
                for tag in block.tags:
                    assert tag.name is not None
                    assert tag.kind is not None
