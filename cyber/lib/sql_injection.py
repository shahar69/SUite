import subprocess


class SQLInjection:
    def __init__(self):
        self.sqlmap_path = '/usr/bin/sqlmap'

    def run_sqlmap(self, target_url, options=None):
        command = [self.sqlmap_path, '-u', target_url]

        if options:
            command.extend(options)

        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
            return output
        except subprocess.CalledProcessError as e:
            return str(e.output)

    def test_vulnerability(self, target_url):
        options = ['--batch', '--level', '5', '--risk', '5']
        return self.run_sqlmap(target_url, options)
