import unittest

import os
import shutil
import tempfile
import uuid
from configparser import ConfigParser

import pygit2

from sundara import sundara
from sundara import config

class TestSundara(unittest.TestCase):

    def setUp(self):
        self.dir = tempfile.mktemp()
        os.makedirs(self.dir)
        self.config_file = os.path.join(self.dir, config.PROJECT_CONF)
        # Make sure user config can't interfere with the tests.
        config.USER_CONF = ''

    def tearDown(self):
        shutil.rmtree(self.dir)

    # Tests for __init__

    def test_uses_config_file_if_possible(self):
        # Make sure a config file exists.
        c = config.Config(self.dir)
        # Embed unique strings.
        unique_md = str(uuid.uuid4())
        unique_generate = str(uuid.uuid4())
        conf = ConfigParser()
        conf.read(self.config_file)
        conf.set('sundara', 'md', unique_md)
        conf.set('sundara', 'generate', unique_generate)
        with open(self.config_file, "w+") as f:
            conf.write(f)
        # Create a Sundara instance and check that it used the values in
        # the config file.
        s = sundara.Sundara(self.dir)
        self.assertEquals(unique_md, s.md_dir)
        self.assertEquals(os.path.join(self.dir, unique_generate), s.generate_path)

    def test_uses_sane_defaults_if_no_config(self):
        # Make sure no config file exists.
        self.assertFalse(os.path.exists(self.config_file))
        # Create a Sundara instance and check that the values are set to
        # sane defaults.
        s = sundara.Sundara(self.dir)
        self.assertEquals('md/', s.md_dir)
        self.assertEquals(os.path.join(self.dir, 'www/'), s.generate_path)

    # Tests for get_files

    def test_get_files_gets_only_md(self):
        # Create git repo with md and other files.
        pygit2.init_repository(self.dir)
        index = pygit2.Repository(self.dir).index
        md_files = [
                'md/index.md',
                'md/footer.md',
                'md/.md.md',
                'md/.test.md',
                'md/test.md',
                'md/test.name.md',
                'md/Test_%*().md'
                'md/tEst.not test.md'
                'md/subdir/test.md',
                'md/subdir.md/test.md',
                'md/.md',
        ]
        bad_files = [
                'notmd/test.md',
                'mdnot/test.md',
                'md/test.md notmd',
                'md/test.html',
                'md/test.MD',
                'MD/test.md',
        ]
        all_files = md_files + bad_files
        for file in all_files:
            try:
                os.makedirs(os.path.join(self.dir,
                    os.path.dirname(file)))
            except OSError:
                pass
            with open(os.path.join(self.dir, file), "w+") as f:
                f.write('\n')
        index.add_all(['*'])
        index.write()
        # Ensure the files were actually created and added to the index.
        for file in all_files:
            self.assertTrue(os.path.isfile(os.path.join(self.dir, file)))
            self.assertTrue(file in index)
        # Create a Sundara instance and make sure get_files ONLY returns
        # the correctly named Markdown files.
        got_files = sundara.Sundara(self.dir).get_files()
        for file in got_files:
            self.assertTrue(os.path.join('md/', file) in md_files)
            self.assertFalse(file in bad_files)
        # Make sure ALL the md files were returned.
        for file in md_files:
            self.assertTrue(file[len('md/'):] in got_files)

    def test_get_files_gets_only_git(self):
        # Create git repo with md files, but only add some of them to
        # the index.
        pygit2.init_repository(self.dir)
        index = pygit2.Repository(self.dir).index
        added_files = [
                'md/index.md',
                'md/.md.md',
                'md/test.md',
                'md/Test_%*().md'
                'md/tEst.not test.md'
                'md/subdir.md/test.md',
        ]
        bad_files = [
                'md/footer.md',
                'md/.test.md',
                'md/test.name.md',
                'md/subdir/test.md',
                'md/.md',
        ]
        all_files = added_files + bad_files
        for file in all_files:
            try:
                os.makedirs(os.path.join(self.dir,
                    os.path.dirname(file)))
            except OSError:
                pass
            with open(os.path.join(self.dir, file), "w+") as f:
                f.write('\n')
        index.add_all(added_files)
        index.write()
        # Ensure the files were actually created and added to the index.
        for file in added_files:
            self.assertTrue(os.path.isfile(os.path.join(self.dir, file)))
            self.assertTrue(file in index)
        # Ensure the bad_files were created but not added to the index.
        for file in bad_files:
            self.assertTrue(os.path.isfile(os.path.join(self.dir, file)))
            self.assertFalse(file in index)
        # Create a Sundara instance and make sure get_files ONLY returns
        # the added_files.
        got_files = sundara.Sundara(self.dir).get_files()
        for file in got_files:
            self.assertTrue(os.path.join('md/', file) in added_files)
            self.assertFalse(os.path.join('md/', file) in bad_files)
        # Make sure ALL the added_files were returned.
        for file in added_files:
            self.assertTrue(file[len('md/'):] in got_files)

    # Tests for generate

    def test_generate_creates_dir_if_not_exists(self):
        pass

    def test_generate_continues_if_dir_exists(self):
        pass

    def test_generate_skips_skipped_files(self):
        pass

    def test_generate_generates_index_html(self):
        pass

    def test_generate_generates_custom_html(self):
        md_files = [
                'md/.md.md',
                'md/.test.md',
                'md/test.md',
                'md/test.name.md',
                'md/Test_%*().md'
                'md/tEst.not test.md'
                'md/subdir/test.md',
                'md/subdir.md/test.md',
                'md/.md',
        ]
        html_files = [
                'www/.md/index.html',
                'www/.test/index.html',
                'www/test/index.html',
                'www/test.name/index.html',
                'www/Test_%*()/index.html'
                'www/tEst.not test/index.html'
                'www/subdir/test/index.html',
                'www/subdir.md/test/index.html',
        ]

    # Tests for init

    #def test_init_excepts_if_config_exists(self):
    #    pass

    def test_init_creates_repo_if_not_exists(self):
        # Don't create a directory or repo.
        project_dir = os.path.join(self.dir, 'TEST')
        self.assertFalse(os.path.exists(project_dir))
        # Make sure init creates it.
        sundara.Sundara(project_dir).init()
        self.assertTrue(os.path.isdir(project_dir))
        self.assertTrue(os.path.isdir(os.path.join(project_dir,
            '.git')))

    def test_init_continues_if_repo_exists(self):
        # Create a repo.
        pygit2.init_repository(self.dir)
        self.assertTrue(os.path.isdir(os.path.join(self.dir, '.git')))
        # Make sure init still runs.
        try:
            sundara.Sundara(self.dir).init()
        except Exception:
            self.fail()

    def test_init_creates_dirs_if_not_exists(self):
        pass

    def test_init_continues_if_dirs_exist(self):
        # Create the dirs.
        os.makedirs(os.path.join(self.dir, 'md/'))
        os.makedirs(os.path.join(self.dir, 'www/'))
        # Make sure init still runs.
        try:
            sundara.Sundara(self.dir).init()
        except Exception:
            self.fail()

    def test_init_creates_files(self):
        pass

    def test_init_continues_if_init_files_exist(self):
        # ..._and_doesnt_overwrite_existing_files
        pass
