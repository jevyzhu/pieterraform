from pytest import raises
from pieterraform.tf_cmder import Terraform
import unittest


class test_tf_mini(unittest.TestCase):
    def test_version(self):
        cmd = Terraform().version().no_color().run().last_run
        assert 'Terraform v0.12.29' == cmd.output[0]

    def test_init(self):
        cmd = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run().last_run
        assert ['terraform', 'init', '-upgrade=false'] == cmd.command

    def test_init_plan(self):
        cmd = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run() \
            .plan().no_color().var('foo', '{a=3 b=4}').run().last_run
        assert ['terraform', 'plan', '-no-color',
                '-var', 'foo={a=3 b=4}'] == cmd.command

    def test_init_plan_apply(self):
        cmd = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run() \
            .plan().no_color().var('foo', '{a=3 b=4}').run() \
            .apply().no_color().run().last_run
        assert ['terraform', 'apply', '-no-color'] == cmd.command

    def test_init_plan_apply_destroy(self):
        run = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run() \
            .plan().no_color().var('foo', '{a=3 b=4}').run() \
            .apply().no_color().run() \
            .destroy().auto_approve().run()
        cmd = run.last_run
        assert ['terraform', 'destroy', '-auto-approve'] == cmd.command
        cmd = run.run_history
        assert ['terraform', 'init', '-upgrade=false'] == cmd[0].command
        assert ['terraform', 'plan', '-no-color',
                '-var', 'foo={a=3 b=4}'] == cmd[1].command
        assert ['terraform', 'apply', '-no-color'] == cmd[2].command

    def test_init_plan_state(self):
        cmd = Terraform().workdir('./tests/tf').fake_run() \
            .init().no_upgrade().run() \
            .plan().no_color().statefile('./state.json').run().last_run
        assert ['terraform', 'plan', '-no-color',
                '-state', './state.json'] == cmd.command
