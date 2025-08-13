import os
import shutil
import unittest

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file


WORKING_DIR = "calculator"
TMP_DIR = os.path.join(WORKING_DIR, "tmp_tests")


class TestGetFilesInfo(unittest.TestCase):
  def test_lists_current_directory(self):
    result = get_files_info(WORKING_DIR, ".")
    self.assertIsInstance(result, str)
    self.assertIn("is_dir=", result)
    # Should include the pkg directory entry
    self.assertIn(" - pkg:", result)

  def test_lists_subdirectory(self):
    result = get_files_info(WORKING_DIR, "pkg")
    self.assertIsInstance(result, str)
    self.assertIn("is_dir=", result)

  def test_rejects_outside_working_directory(self):
    result_abs = get_files_info(WORKING_DIR, "/bin")
    result_parent = get_files_info(WORKING_DIR, "../")
    self.assertIn("Error:", result_abs)
    self.assertIn("outside the permitted working directory", result_abs)
    self.assertIn("Error:", result_parent)
    self.assertIn("outside the permitted working directory", result_parent)


class TestGetFileContent(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    os.makedirs(TMP_DIR, exist_ok=True)
    with open(os.path.join(TMP_DIR, "readable.txt"), "w") as f:
      f.write("hello world")

  @classmethod
  def tearDownClass(cls):
    if os.path.isdir(TMP_DIR):
      shutil.rmtree(TMP_DIR)

  def test_reads_existing_file(self):
    path = os.path.join("tmp_tests", "readable.txt")
    content = get_file_content(WORKING_DIR, path)
    self.assertEqual(content, "hello world")

  def test_missing_file_returns_error(self):
    content = get_file_content(WORKING_DIR, "pkg/does_not_exist.py")
    self.assertIn("Error:", content)
    self.assertIn("File not found", content)

  def test_outside_working_directory_error(self):
    content = get_file_content(WORKING_DIR, "/bin/cat")
    self.assertIn("Error:", content)
    self.assertIn("outside the permitted working directory", content)


class TestWriteFile(unittest.TestCase):
  @classmethod
  def tearDownClass(cls):
    if os.path.isdir(TMP_DIR):
      shutil.rmtree(TMP_DIR)

  def test_write_within_working_directory(self):
    rel_path = os.path.join("tmp_tests", "note.txt")
    message = write_file(WORKING_DIR, rel_path, "test note")
    self.assertIn("Successfully wrote", message)
    full_path = os.path.join(WORKING_DIR, rel_path)
    with open(full_path, "r") as f:
      self.assertEqual(f.read(), "test note")

  def test_write_outside_working_directory(self):
    message = write_file(WORKING_DIR, "/tmp/outside.txt", "nope")
    self.assertIn("Error:", message)
    self.assertIn("outside the permitted working directory", message)


class TestRunPythonFile(unittest.TestCase):
  def test_run_valid_python_file(self):
    result = run_python_file(WORKING_DIR, "main.py")
    self.assertIn("STDOUT:", result)
    self.assertIn("17", result)
    self.assertNotIn("Process exited with code", result)

  def test_run_python_file_with_args(self):
    result = run_python_file(WORKING_DIR, "main.py", ["3 + 5"])
    self.assertIn("STDOUT:", result)
    self.assertIn("17", result)

  def test_nonexistent_file(self):
    result = run_python_file(WORKING_DIR, "nonexistent.py")
    self.assertIn("Error:", result)
    self.assertIn("not found", result)

  def test_non_python_file(self):
    result = run_python_file(WORKING_DIR, "lorem.txt")
    self.assertIn("Error:", result)
    self.assertIn("is not a Python file", result)

  def test_outside_working_directory(self):
    result = run_python_file(WORKING_DIR, "../main.py")
    self.assertIn("Error:", result)
    self.assertIn("outside the permitted working directory", result)


if __name__ == "__main__":
  unittest.main(verbosity=2)
