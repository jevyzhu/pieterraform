import logging
import pathlib
from pytest import raises
from pieterraform import Terraform, TfState
import unittest


class test_tf_mini(unittest.TestCase):
    def test_version(self):
        results = Terraform().version().run().results
        assert 'Terraform v0.13.0' == results[-1].output[0]

    def test_init(self):
        results = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run().results
        assert ['terraform', 'init', '-upgrade=false'] == results[-1].command

    def test_init_dir(self):
        results = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().dir('prod').run().results
        assert ['terraform', 'init', '-upgrade=false',
                'prod'] == results[-1].command

    def test_init_plan(self):
        one_run = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run() \
            .plan().no_color().var('foo', '{a=3 b=4}').run()

        assert ['terraform', 'plan', '-no-color', '-var',
                'foo={a=3 b=4}'] == one_run.results[-1].command

    def test_init_plan_dir(self):
        one_run = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().dir('prod').run() \
            .plan().no_color().dir('prod').var('foo', '{a=3 b=4}').run()

        assert ['terraform', 'plan', '-no-color', '-var',
                'foo={a=3 b=4}', 'prod'] == one_run.results[-1].command

    def test_init_plan_apply(self):
        one_run = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run() \
            .plan().var('foo', '{a=3 b=4}').dir('prod').run() \
            .apply().no_color().run()
        command = one_run.last_result.command
        assert ['terraform', 'apply', '-no-color'] == command
        command = one_run.results[1].command
        assert ['terraform', 'plan', '-var', 'foo={a=3 b=4}',
                'prod'] == command

    def test_init_plan_apply_dir(self):
        one_run = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run() \
            .plan().var('foo', '{a=3 b=4}').dir('prod').run() \
            .apply().no_color().dir('prod').run()
        command = one_run.last_result.command
        assert ['terraform', 'apply', '-no-color', 'prod'] == command
        command = one_run.results[1].command
        assert ['terraform', 'plan', '-var', 'foo={a=3 b=4}',
                'prod'] == command

    def test_init_plan_apply_destroy(self):
        one_run = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run() \
            .plan().no_color().var('foo', '{a=3 b=4}').out('me').var('c', '5').run() \
            .apply().no_color().use_plan('me').run() \
            .destroy().auto_approve().statefile('me').run()
        command = one_run.last_result.command
        assert ['terraform', 'destroy', '-auto-approve', '-state',
                'me'] == command
        command = one_run.results[0].command
        assert ['terraform', 'init', '-upgrade=false'] == command
        command = one_run.results[1].command
        assert [
            'terraform', 'plan', '-no-color', '-var', 'foo={a=3 b=4}', '-out',
            'me', '-var', 'c=5'
        ] == command
        command = one_run.results[2].command
        assert ['terraform', 'apply', '-no-color', 'me'] == command

    def test_init_plan_apply_destroy_dir(self):
        one_run = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run() \
            .plan().no_color().var('foo', '{a=3 b=4}').out('me').var('c', '5').run() \
            .apply().no_color().use_plan('me').run() \
            .destroy().auto_approve().dir('prod').statefile('me').run()
        command = one_run.last_result.command
        assert ['terraform', 'destroy', '-auto-approve', '-state',
                'me', 'prod'] == command
        command = one_run.results[0].command
        assert ['terraform', 'init', '-upgrade=false'] == command
        command = one_run.results[1].command
        assert [
            'terraform', 'plan', '-no-color', '-var', 'foo={a=3 b=4}', '-out',
            'me', '-var', 'c=5'
        ] == command
        command = one_run.results[2].command
        assert ['terraform', 'apply', '-no-color', 'me'] == command

    def test_init_plan_state(self):
        command = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run() \
            .plan().statefile('./state.json').no_color().run() \
            .last_result.command
        assert ['terraform', 'plan', '-no-color', '-state',
                './state.json'] == command


class test_tf_state(unittest.TestCase):
    def test_1(self):
        state_file_path = pathlib.Path(
            __file__).parents[0].joinpath('terraform.tfstate')
        t = TfState(state_file_path)
        assert t.output.bastion_ip
        assert t.output.database_ip
        assert t.output.filestore_ip
        assert t.output.filestore_share_name
