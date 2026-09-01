import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
SWARM_PATH = ROOT / '.brain' / 'scripts' / 'swarm.py'
NOTEBOOK_PATH = ROOT / '.brain' / 'scripts' / 'notebook_context.py'


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class SwarmPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.swarm = load_module(SWARM_PATH, 'swarm_mod')
        cls.notebook = load_module(NOTEBOOK_PATH, 'notebook_mod')

    def test_plan_escalates_security_task(self):
        plan = self.swarm.build_plan(
            task='Design authentication security architecture for cross-boundary refactor',
            files=['backend/CONTEXT.md', '.brain/RULES.md'],
            notebook_id='nb-1',
        )
        self.assertEqual(plan['tier'], 'frontier')
        self.assertEqual(plan['worker_count'], 2)
        self.assertIn('planner', [r['role'] for r in plan['roles']])
        self.assertEqual(plan['notebook']['id'], 'nb-1')
        self.assertEqual(len(plan['context_files']), 2)

    def test_execute_writes_run_artifacts_and_db(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'work').mkdir()
            (root / '.brain' / 'swarm').mkdir(parents=True)
            plan = self.swarm.build_plan('Implement routing', ['AGENTS.md'], 'nb-2')
            result = self.swarm.execute_plan(root=root, plan=plan)
            run_dir = Path(result['run_dir'])
            self.assertTrue((run_dir / 'plan.json').is_file())
            self.assertTrue((run_dir / 'worker-1.md').is_file())
            self.assertTrue((run_dir / 'reviewer.md').is_file())
            conn = sqlite3.connect(root / '.brain' / 'swarm' / 'swarm.sqlite')
            try:
                row = conn.execute('select count(*) from plans').fetchone()[0]
            finally:
                conn.close()
            self.assertEqual(row, 1)

    def test_distill_note_uses_wikilinks(self):
        note = self.notebook.render_note(
            title='OpenRouter Routing',
            notebook_title='AI Routing, Agent Skills, and Context Engineering Strategies',
            question='How should we route models?',
            answer='Use planner plus workers.',
            links=['[[swarm]]', '[[routing]]'],
        )
        self.assertIn('[[swarm]]', note)
        self.assertIn('NotebookLM', note)
        self.assertIn('# OpenRouter Routing', note)


if __name__ == '__main__':
    unittest.main()
