#!/usr/bin/env python3 
import argparse
import boto3
import os
import re

from botocore.exceptions import ClientError

class Replaceroni:
    '''Replaceroni is a utility class for the replacing of templated secret names in 
    a text file'''
    def __init__(self, filename):
        self.secretsmanager_client = boto3.Session(profile_name='EvergreenAdmins'
                ).client('secretsmanager')
        self.file= open(filename)
        self.outfile_string = ""

    def get_value(self, name, stage=None):
        '''
        get_value gets the value of a secret from AWS secret manager.
    
        :param client: secretsmanager object
        :param name: The name of the secret to retrieve. Required.
        :param stage: The stage of the secret to retrieve. If this is None, the
                      current stage is retrieved.
        :return: The value of the secret. When the secret is a string, the value is
                 contained in the `SecretString` field. When the secret is bytes,
                 it is contained in the `SecretBinary` field.
        '''
        if name is None:
            raise ValueError
        try:
            kwargs = {'SecretId': name}
            if stage is not None:
                kwargs['VersionStage'] = stage
            response = self.secretsmanager_client.get_secret_value(**kwargs)
        except ClientError:
            raise ValueError('Couldn\'t get value for secret %s.', name)
        else:
            return response
    
    def replace_templates(self):
        '''
        replace_templates will replace all templates found in the line
        with the AWS value, until none remain.
        '''

        for line in self.file:
            template = re.search('{{(.*)}}',line)
            while template:
                secret_name = template.group(1)
                secret_value = self.get_value(secret_name)['SecretString']
                line = re.sub('{{'+secret_name+'}}',secret_value,line)
                template = re.search('{{(.*)}}',line)
            self.outfile_string += line

    def print_outfile(self):
        print(self.outfile_string)

def main():
    parser = argparse.ArgumentParser(
    description='This script takes in a JSON environment variable file with templated secret names, '
        'replaces the secret names with secrets using the AWS CLI, and finally prints this to stdout.'
        'The templating format should be something like {{secretname}}. '
        'You will need to set up and authenticate using the method explained in BUILD-13246 '
        'before running this. '
        'Sample usage: pipenv run ./replace_json_secrets.py sample_template_file.json > secrets_file.json'
        )
    parser.add_argument(
        'template', help='template file')
    args = parser.parse_args()
    replaceronus = Replaceroni(args.template)
    replaceronus.replace_templates()
    replaceronus.print_outfile()

if __name__ == '__main__':
    main()
