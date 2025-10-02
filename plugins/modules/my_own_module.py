#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Module creates txt file on remote host using `path` and `content` params.

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This module creates text file on remote host using path specified in `path` and content specified in `content` params.

options:
    path:
        description: This is the path to the file to create.
        required: true
        type: str
    content:
        description:
            - Content of the file to create.
        required: true
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - ns.my_own_collection.my_doc_fragment_name

author:
    - Nikita Sardov (@nikitasardov)
'''

EXAMPLES = r'''
# Pass in a path
- name: Create file with content
  ns.my_own_collection.my_own_module:
    path: /tmp/hello.txt

# pass in a path and content
- name: Test with a message and changed output
  ns.my_own_collection.my_own_module:
    path: /tmp/hello.txt
    content: hello world

# fail the module
- name: Test failure of the module
  ns.my_own_collection.my_own_module:
    path: true
    content: hello world
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original path param that was passed in.
    type: str
    returned: always
    sample: '/tmp/hello.txt'
message:
    description: The output message that the module generates.
    type: str
    returned: always
    sample: 'File created successfully'
'''


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)

    import os

    file_path = module.params['path']
    file_content = module.params.get('content', '')

    result['original_message'] = file_path

    # Check if file already exists and has the same content
    file_exists = os.path.exists(file_path)
    content_changed = True

    if file_exists:
        try:
            with open(file_path, 'r') as f:
                existing_content = f.read()
            content_changed = existing_content != file_content
        except Exception as e:
            module.fail_json(
                msg=f'Failed to read existing file: {str(e)}', **result)

    # Create or update the file if needed
    if not file_exists or content_changed:
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w') as f:
                f.write(file_content)

            result['changed'] = True
            result['message'] = f'File {"created" if not file_exists else "updated"} successfully'
        except Exception as e:
            module.fail_json(msg=f'Failed to write file: {str(e)}', **result)
    else:
        result['message'] = 'File already exists with the same content'

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
