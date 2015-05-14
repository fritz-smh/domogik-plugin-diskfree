# -*- coding: utf-8 -*-

### common imports
from flask import Blueprint, abort
from domogik.common.utils import get_packages_directory
from domogik.admin.application import render_template
from domogik.admin.views.clients import get_client_detail
from jinja2 import TemplateNotFound

### package specific imports
import subprocess



### package specific functions
def get_df():
    df = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    #device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
    if isinstance(output, str):
        output = unicode(output, 'utf-8')
    return output




### common tasks
package = "plugin_diskfree"
template_dir = "{0}/{1}/admin/templates".format(get_packages_directory(), package)
static_dir = "{0}/{1}/admin/static".format(get_packages_directory(), package)

plugin_diskfree_adm = Blueprint(package, __name__,
                        template_folder = template_dir,
                        static_folder = static_dir)

@plugin_diskfree_adm.route('/<client_id>')
def index(client_id):
    client_id = "plugin-diskfree.darkstar"
    detail = get_client_detail(client_id)
    try:
        #return render_template('{0}.html'.format(page))
        return render_template('plugin_diskfree.html',
            clientid = client_id,
            client_detail = detail,
            mactive="clients",
            active = 'advanced',
            df = get_df())

    except TemplateNotFound:
        abort(404)

