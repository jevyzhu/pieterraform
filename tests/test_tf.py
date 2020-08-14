import logging
from pytest import raises
from pieterraform import Terraform
import unittest


class test_tf_mini(unittest.TestCase):
    def test_version(self):
        results = Terraform().version().no_color().run().results
        assert 'Terraform v0.13.0' == results[-1].output[0]

    def test_init(self):
        results = Terraform().workdir('./tests/tf').fake_run() \
        .init().no_upgrade().run().results
        assert ['terraform', 'init', '-upgrade=false'] == results[-1].command

    def test_init_plan(self):
        one_run = Terraform().workdir('./tests/tf').fake_run() \
        .init().no_upgrade().run() \
        .plan().no_color().var('foo', '{a=3 b=4}').run()

        assert ['terraform', 'plan', '-no-color', '-var',
                'foo={a=3 b=4}'] == one_run.results[-1].command

    def test_init_plan_apply(self):
        last_result = Terraform().workdir('./tests/tf').fake_run() \
        .init().no_upgrade().run() \
        .plan().no_color().var('foo', '{a=3 b=4}').run() \
        .apply().no_color().run().last_result
        assert ['terraform', 'apply', '-no-color'] == last_result.command

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
            'terraform', 'plan', '-no-color',
            '-var', 'foo={a=3 b=4}',
            '-out', 'me',
            '-var', 'c=5'
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
