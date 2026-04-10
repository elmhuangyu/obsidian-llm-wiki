import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml
from state import (
  collect_candidates,
  compute_sha1,
  find_pending,
  load_state,
  needs_processing,
  record_failure,
  record_success,
  save_state,
)


class TestState(unittest.TestCase):
  def setUp(self):
    self.test_dir = Path(tempfile.mkdtemp())
    self.state_file = self.test_dir / "state.yaml"
    self.test_file = self.test_dir / "test.txt"
    self.test_file.write_text("hello world")

  def tearDown(self):
    shutil.rmtree(self.test_dir)

  def test_compute_sha1(self):
    expected_hash = hashlib.sha1(b"hello world").hexdigest()
    self.assertEqual(compute_sha1(self.test_file), expected_hash)

  def test_load_state_empty(self):
    self.assertEqual(load_state(self.state_file), {})

  def test_load_state_existing(self):
    state_data = {"test.txt": {"sha1": "123"}}
    with open(self.state_file, "w") as f:
      yaml.dump(state_data, f)
    self.assertEqual(load_state(self.state_file), state_data)

  def test_save_state(self):
    state_data = {"test.txt": {"sha1": "123"}}
    save_state(state_data, self.state_file)
    self.assertTrue(self.state_file.exists())
    with open(self.state_file) as f:
      loaded = yaml.safe_load(f)
    self.assertEqual(loaded, state_data)

  def test_needs_processing_new_file(self):
    self.assertTrue(needs_processing(self.test_file, {}))

  def test_needs_processing_changed_file(self):
    old_hash = "not_the_real_hash"
    state = {self.test_file.name: {"sha1": old_hash}}
    self.assertTrue(needs_processing(self.test_file, state))

  def test_needs_processing_unchanged_file(self):
    real_hash = compute_sha1(self.test_file)
    state = {self.test_file.name: {"sha1": real_hash}}
    self.assertFalse(needs_processing(self.test_file, state))

  def test_collect_candidates(self):
    # Create some other files
    (self.test_dir / "test.md").write_text("markdown")
    (self.test_dir / "ignore.png").write_text("image")

    candidates = collect_candidates(self.test_dir, [".txt", ".md"])
    self.assertEqual(len(candidates), 2)
    candidate_names = {c.name for c in candidates}
    self.assertIn("test.txt", candidate_names)
    self.assertIn("test.md", candidate_names)

  def test_find_pending(self):
    (self.test_dir / "test.md").write_text("markdown")
    txt_hash = compute_sha1(self.test_file)

    # txt file is unchanged, md file is new
    state = {self.test_file.name: {"sha1": txt_hash}}
    candidates = [self.test_file, self.test_dir / "test.md"]

    pending = find_pending(candidates, state)
    self.assertEqual(len(pending), 1)
    self.assertEqual(pending[0].name, "test.md")

  def test_record_success(self):
    state = {}
    record_success(self.test_file, state, "processed", output="out.md")
    self.assertIn(self.test_file.name, state)
    item = state[self.test_file.name]
    self.assertEqual(item["status"], "processed")
    self.assertEqual(item["output"], "out.md")
    self.assertEqual(item["path"], str(self.test_file))
    self.assertEqual(item["sha1"], compute_sha1(self.test_file))

  def test_record_failure(self):
    state = {}
    record_failure(self.test_file, state)
    self.assertIn(self.test_file.name, state)
    item = state[self.test_file.name]
    self.assertEqual(item["status"], "failed")
    self.assertEqual(item["path"], str(self.test_file))
    self.assertNotIn("sha1", item)


if __name__ == "__main__":
  unittest.main()
