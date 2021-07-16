# AWS_Secret_Templating

This script takes in a JSON environment variable file with templated secret names, replaces the secret names with secrets using the AWS CLI, and finally prints this to stdout.

The templating format should be something like `{{secretname}}`.
An example exists in the repo.

You will need to set up and authenticate using the method explained in BUILD-13246 before running this.

Sample usage: 
`pipenv run ./replace_json_secrets.py sample_template_file.json > secrets_file.json`
